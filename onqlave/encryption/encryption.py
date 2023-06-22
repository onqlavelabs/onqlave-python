import logging

# from logger.logger import OnqlaveLogging
from keymanager.random_service import CSPRNG
from keymanager.id_service import IDService
from keymanager.key_manager_client import KeyManager,Configuration
from encryption.options import DebugOption,ArxOption
from connection.client import RetrySettings
from credentials.credentials import Credential
from keymanager.onqlave_types.types import Aesgcm128,Aesgcm256,XChacha20poly1305
from keymanager.factories.aes_gcm_factory import AEADGCMKeyFactory
from keymanager.factories.xchacha20_poly1305_factory import XChaCha20Poly1305KeyFactory
from keymanager.operations.aes_128_gcm_operation import AesGcmKeyOperation
from keymanager.operations.aes_256_gcm_operation import Aes256GcmKeyOperation
from keymanager.operations.xchacha20_poly1305_operation import XChaCha20Poly1305KeyOperation

class Encryption:
    """A class that models the encryption services with 2 main groups of features:
    - Encrypt/Decrypt data blocks
    - Encrypt/Decrypt data streams
    Before actually begin the encrypt/decrypt, it requires an init step for these operations
    """

    def __init__(self, 
                 debug_option: DebugOption,
                 arx_option: ArxOption,
                 credential_option: Credential,
                 retry_setting: RetrySettings) -> None:
        """ Init an instance of the encryption service with the following params:
        option = {credentials, retryoptions, arx_url}
        logger
        random_number_generation_service
        id_gen_service
        aead_gcm_key_factory
        x_ch_cha_key_factory 

        """
        self._logger = logging.getLogger(self.__class__.__name__)
        # random service
        self._csprng = CSPRNG()
        # id gen
        self._id_generator = IDService()
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
    def init_encrypt_operation(self, operation: str) -> None:
        """Return the algorithm and primitives of the encrypt operation
        """
        # get the edk, dk, algo from Onqlave keymanager
        self._key_mamanger.fetch_encryption_key()
        #
        pass

    def init_decrypt_operation(self) -> None:
        pass

    # encrypt/decrypt
    def encrypt(self) -> None:
        #
        operation = "Encrypt"
        self.init_encrypt_operation(operation=operation)
        pass

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
