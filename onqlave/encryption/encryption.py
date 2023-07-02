import logging
import io
# from logger.logger import OnqlaveLogging
from keymanager.random_service import CSPRNG
from keymanager.id_service import IDService
from keymanager.key_manager_client import KeyManager
from connection.connection import Configuration
from encryption.options import DebugOption,ArxOption
from connection.client import RetrySettings
from credentials.credentials import Credential

from encryption.plain_stream_processor import PlainStreamProcessor

from keymanager.onqlave_types.types import Aesgcm128,Aesgcm256,XChacha20poly1305,AlgorithmSerialiser
from keymanager.factories.aes_gcm_factory import AEADGCMKeyFactory
from keymanager.factories.xchacha20_poly1305_factory import XChaCha20Poly1305KeyFactory
from keymanager.operations.aes_128_gcm_operation import AesGcmKeyOperation
from keymanager.operations.aes_256_gcm_operation import Aes256GcmKeyOperation
from keymanager.operations.xchacha20_poly1305_operation import XChaCha20Poly1305KeyOperation


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
        self._logger = logging.getLogger(self.__class__.__name__)
        # random service
        self._csprng = CSPRNG()
        # id gen
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
        self._key_mamanger = KeyManager(configuration=self._option,random_service=self._csprng)
        
        self._aead_gcm_key_factory = AEADGCMKeyFactory(id_service=self._id_generator, random_service=self._csprng)
        self._xchcha_key_factory = XChaCha20Poly1305KeyFactory(id_service=self._id_generator, random_service=self._csprng)

        self._operations = {
            Aesgcm128:AesGcmKeyOperation(key_factory=self._aead_gcm_key_factory),
            Aesgcm256:Aes256GcmKeyOperation(key_factory=self._aead_gcm_key_factory),
            XChacha20poly1305:XChaCha20Poly1305KeyOperation(key_factory=self._xchcha_key_factory)
        }

    # impl setters & getters

    # init encrypt/decrypt operations
    def init_encrypt_operation(self, operation: str):
        """Init the encrypt operation by getting the required data including: algorithm, primitives, keys of the encrypt operation

        Args:
            operation: a string describe the name of the operation
        
        Returns:
            The algorithm & primitive

        """
        # get the edk, dk, algo from Onqlave keymanager
        edk, dk, algo = self._key_mamanger.fetch_encryption_key()
        ops = self._operations[algo]
        
        factory = ops.get_factory()
        key = factory.new_key_from_data(ops,dk)

        primitive = factory.primitive(key)

        algorithm = AlgorithmSerialiser(version=0,algo=algo,key=edk)

        return algorithm, primitive

    def init_decrypt_operation(self) -> None:
        pass

    # encrypt/decrypt
    def encrypt(self, plaintext: bytearray, associated_data: bytearray) -> bytes:
        """ Encrypt plaintext (as a bytearray) with the combination of associated_data

        Args:
            plaintext: a bytearray contains the plain data that needs to be encrypted
            associated_data: a bytearray contains the associated data that is going to be
            used before the encryption process happens

        Returns:
            the value of the cipher as bytes

        """
        operation = "Encrypt"
        
        header, primitive = self.init_encrypt_operation(operation=operation)
        
        cipher_data = primitive.encrypt(
            plaintext=plaintext,
            associated_data=associated_data 
        ) # should try-catch error if neccessary
        print(f"cipher data = {cipher_data}")
        
        cipher_stream = io.BytesIO()
        processor = PlainStreamProcessor(cipher_stream=cipher_stream)
        processor.write_header(header)
        processor.write_packet(cipher_data)
        
        # log a debug line here
        return cipher_stream.getvalue()

    def derypt(self) -> None:
        pass

    # encrypt/decrypt stream
    def encrypt_stream(self) -> None:
        pass

    def derypt_stream(self) -> None:
        pass

    # encrypt/decrypts structure
    def encrypt_structure(self) -> None:
        pass

    def derypt_structure(self) -> None:
        pass
