import io
from datetime import datetime
# from onqlave.logger.logger import OnqlaveLogging
from onqlave.keymanager.random_service import CSPRNG
from onqlave.keymanager.id_service import IDService
from onqlave.keymanager.key_manager_client import KeyManager
from onqlave.connection.connection import Configuration
from onqlave.encryption.options import DebugOption,ArxOption
from onqlave.connection.client import RetrySettings
from onqlave.credentials.credentials import Credential

from onqlave.encryption.plain_stream_processor import PlainStreamProcessor
from onqlave.encryption.encrypted_stream_processor import EncryptedStreamProcessor

from onqlave.logger.logger import OnqlaveLogger

from onqlave.keymanager.onqlave_types.types import Aesgcm128,Aesgcm256,XChacha20poly1305
from onqlave.keymanager.onqlave_types.types import AlgorithmSerialiser, AlgorithmDeserialiser
from onqlave.keymanager.factories.aes_gcm_factory import AEADGCMKeyFactory
from onqlave.keymanager.factories.xchacha20_poly1305_factory import XChaCha20Poly1305KeyFactory
from onqlave.keymanager.operations.aes_128_gcm_operation import AesGcmKeyOperation
from onqlave.keymanager.operations.aes_256_gcm_operation import Aes256GcmKeyOperation
from onqlave.keymanager.operations.xchacha20_poly1305_operation import XChaCha20Poly1305KeyOperation
from onqlave.errors.errors import OnqlaveError, FetchEncryptionKeyException
from onqlave.errors.errors import OperationMappingException, CreatingKeyException, CreatingPrimitiveException, FetchDecryptionKeyException, EncryptionOperationException
from onqlave.messages import messages


class Encryption:
    """A class that models the encryption services with 2 main groups of features:
    - Encrypt/Decrypt data blocks
    - Encrypt/Decrypt data streams
    Before actually begin the encrypt/decrypt, it requires an inititalisation step for these operations
    """

    def __init__(self, 
                 debug_option: DebugOption,
                 arx_option: ArxOption,
                 credential_option: Credential,
                 retry_setting: RetrySettings) -> None:
        """ Init an instance of the encryption service

        Args:
            debug_option: specify the preffered debug optionn
            arx_option: specify the configuration of the arx
            credential_option: specify the credentials
            retry_setting: specify the retry setting

        Returns:
            Nothing
        """
        self._logger = OnqlaveLogger(debug_option.get_debug_option())
        # random service
        self._csprng = CSPRNG()
        
        self._id_generator = IDService(self._csprng)
        index = arx_option.get_arx_url().rindex("/") # do sth to find the last index of the "/"
        arx_url = arx_option.get_arx_url()[:index]
        arx_id = arx_option.get_arx_url()[index+1:]
        self._option = Configuration(
            credentials=credential_option,
            retry_settings=retry_setting,
            arx_url=arx_url, 
            arx_id=arx_id
        )
        self._key_mamanger = KeyManager(
            configuration=self._option,
            random_service=self._csprng,
            debug_option=debug_option
        )
        
        self._aead_gcm_key_factory = AEADGCMKeyFactory(
            id_service=self._id_generator, 
            random_service=self._csprng
        )

        self._xchcha_key_factory = XChaCha20Poly1305KeyFactory(
            id_service=self._id_generator, 
            random_service=self._csprng
        )

        self._operations = {
            Aesgcm128:AesGcmKeyOperation(key_factory=self._aead_gcm_key_factory),
            Aesgcm256:Aes256GcmKeyOperation(key_factory=self._aead_gcm_key_factory),
            XChacha20poly1305:XChaCha20Poly1305KeyOperation(key_factory=self._xchcha_key_factory)
        }


    def init_encrypt_operation(self, operation: str):
        """Init the encrypt operation by getting the required data including: algorithm, primitives, keys of the encrypt operation

        Args:
            operation: a string describe the name of the operation
        
        Returns:
            The algorithm & primitive

        """
        edk, dk, algo = self._key_mamanger.fetch_encryption_key()        
        try:
            ops = self._operations[algo]
        except Exception:
            raise OperationMappingException(
                message=messages.OPERATION_MAPPING_EXCEPTION,
                original_error=None,
                code=OnqlaveError.SdkErrorCode
            )

        try:
            factory = ops.get_factory()
            key = factory.new_key_from_data(ops,dk)
        except Exception:
            raise CreatingKeyException(
                message=messages.CREATING_KEY_EXCEPTION,
                original_error=None,
                code=OnqlaveError.SdkErrorCode
            )
        
        try:
            primitive = factory.primitive(key)
        except Exception:
            raise CreatingPrimitiveException(
                message=messages.CREATING_PRIMITIVE_EXCEPTION,
                original_error=None,
                code=OnqlaveError.SdkErrorCode
            )

        algorithm = AlgorithmSerialiser(version=0,algo=algo,key=edk)

        return algorithm, primitive

    def init_decrypt_operation(self, operation: str, algo: AlgorithmDeserialiser):
        """Init the decrypt operation by fetching the decryption key from the Onqlave Platform,
        then init the key factory and encryption primitives

        Args:
            operation: a string indicates the name/type of the operation
            algo: a specified object contains the information about the selected algorithm

        Returns:
            The encryption primitive object
        """
        
        dk = self._key_mamanger.fetch_decryption_key(algo._key)
        
        try:
            ops = self._operations[algo.algorithm()]
        except Exception as exc:
            raise OperationMappingException(
                messages=messages.OPERATION_MAPPING_EXCEPTION,
                original_error=None,
                code=OnqlaveError.SdkErrorCode
            )
        
        try:
            factory = ops.get_factory()
            key = factory.new_key_from_data(ops, dk)
            primitive = factory.primitive(key)
        except Exception:
            raise EncryptionOperationException(
                message=messages.ENCRYPTION_OPERATION_FAILED,
                original_error=None,
                code=OnqlaveError.SdkErrorCode
            )
        
        return primitive

    def encrypt(self, plaintext: bytearray, associated_data: bytearray) -> bytes:
        """ Encrypt plaintext (as a bytearray) with the combination of associated_data
        regarding to the application of AEAD - Authenticated Encryption with Associated Data

        Args:
            plaintext: a bytearray contains the plain data that needs to be encrypted
            associated_data: a bytearray contains the associated data that is going to be
            used for the authentication

        Returns:
            the value of the cipher as bytes

        """
        operation = "Encrypt"
        start = datetime.utcnow()
        self._logger.log_debug(messages.ENCRYPTING_OPERATION.format(operation))
        header, primitive = self.init_encrypt_operation(operation=operation)
        
        cipher_data = primitive.encrypt(
            plaintext=plaintext,
            associated_data=associated_data 
        )
        if cipher_data is None:
            self._logger.log_error(message=messages.ENCRYPTION_EXCEPTION)
            return None
        
        cipher_stream = io.BytesIO()
        processor = PlainStreamProcessor(cipher_stream=cipher_stream)
        processor.write_header(header)
        processor.write_packet(cipher_data)
        
        finish = datetime.utcnow()
        self._logger.log_debug(messages.ENCRYPTED_OPERATION.format(operation,str(f'{(finish-start).seconds} secs and {(finish-start).microseconds} microsecs')))
        return cipher_stream.getvalue()

    def decrypt(self, cipher_data: bytearray, associated_data: bytearray):
        """Decrypt data (as a bytearray) under the AEAD

        Args:
            cipher_data: a bytearray contains the encrypted data that needs to be decrypted
            associated_data: a bytearray contains the associated data that is going to be
            used for the authentication

        Returns:
            The decrypted data
        """
        operation = "Decrypt"
        start = datetime.utcnow()
        self._logger.log_debug(messages.DECRYPTING_OPERATION.format(operation))

        cipher_stream = io.BytesIO(initial_bytes=cipher_data)
        processor = EncryptedStreamProcessor(cipher_stream)
        # shoul try-catch this command
        algo = processor.read_header()
        if algo is None:
            self._logger.log_error(message=messages.ENCRYPTED_STREAM_READ_HEADER_EXCEPTION)
            return None

        # maybe this one need try-catch?
        primitive = self.init_decrypt_operation(operation, algo)

        cipher = processor.read_packet()
        if cipher is None:
            self._logger.log_error(message=messages.ENCRYPTED_STREAM_READ_PACKET_EXCEPTION)
            return None
        
        plain_data = primitive.decrypt(cipher, associated_data)
        if plain_data is None:
            self._logger.log_error(message=messages.DECRYPTION_EXCEPTION)
            return None # decryption error

        # log a debug line

        finish = datetime.utcnow()
        self._logger.log_debug(messages.DECRYPTED_OPERATION.format(operation,str(f'{(finish-start).seconds} secs and {(finish-start).microseconds} microsecs')))
        return plain_data

    # encrypt/decrypt stream
    def encrypt_stream(
            self, 
            plain_stream: io.BytesIO, 
            cipher_stream: io.BytesIO,
            associated_data: bytearray
    ) -> None:
        """Encrypt the plainstream and output the result into the cipherstream

        Args:
            plain_stream: a standard Python stream object contains the plain data
            cipher_stream: a standard Python stream object contains the encrypted data
            associated_data: additional data (as a bytearray) for authentication purpose (AEAD)

        Returns:
            Nothing
        """
        operation = "EncryptStream"
        start = datetime.utcnow()
        self._logger.log_debug(messages.ENCRYPTING_OPERATION.format(operation))
        
        header, primitive = self.init_encrypt_operation(operation)
        processor = PlainStreamProcessor(cipher_stream)
        processor.write_header(header)
        temp_buffer = bytearray(32*1024)

        while True:
            
            data_len = plain_stream.readinto(temp_buffer)
            if data_len == 0:
                break
            
            cipher_text = primitive.encrypt(temp_buffer[:data_len],associated_data)
            if cipher_text is None:
                self._logger.log_error(message=messages.ENCRYPTION_EXCEPTION)
                break
            processor.write_packet(cipher_text)

        finish = datetime.utcnow()
        self._logger.log_debug(messages.ENCRYPTED_OPERATION.format(operation,str(f'{(finish-start).seconds} secs and {(finish-start).microseconds} microsecs')))

            


    def decrypt_stream(
            self,
            cipher_stream: io.BytesIO,
            plain_stream: io.BytesIO,
            associated_data: bytearray
    ) -> None:
        """Decrypt the encrypted stream and output the result into the plain stream

        Args:
            cipher_stream: a standard Python stream object contains the encrypted data
            plain_stream: a standard Python stream object contains the plain data
            associated_data: additional data (as a bytearray) for authentication purpose (AEAD)

        Returns:
            Nothing
        """
        operation = "DecryptStream"
        start = datetime.utcnow()
        self._logger.log_debug(messages.DECRYPTING_OPERATION.format(operation))

        processor = EncryptedStreamProcessor(cipher_stream)
        cipher_stream.seek(0)
        algo = processor.read_header()
        if algo is None:
            self._logger.log_error(message=messages.ENCRYPTED_STREAM_READ_HEADER_EXCEPTION)
            return None
        primitive = self.init_decrypt_operation(operation,algo)
        
        while True:
            
            ciphertext = processor.read_packet()
            if ciphertext is None:
                break

            plain_data = primitive.decrypt(ciphertext, associated_data)
            if plain_data is None:
                self._logger.log_error(message=messages.DECRYPTION_EXCEPTION)
                break

            plain_stream.write(plain_data)
        finish = datetime.utcnow()
        self._logger.log_debug(messages.DECRYPTED_OPERATION.format(operation,str(f'{(finish-start).seconds} secs and {(finish-start).microseconds} microsecs')))
