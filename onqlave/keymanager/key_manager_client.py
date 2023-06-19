import logging

from credentials.credentials import Credential
from connection.client import RetrySettings
from utils.hasher import Hasher
# from logger.logger import OnqlaveLogging
from connection.connection import Connection
from keymanager.factories.rsa_ssa_pkcs1_sha_factory import RSASSAPKCS1SHAKeyFactory
from keymanager.random_service import CSPRNG
from keymanager.onqlave_types.types import RsaSsapkcs12048sha256f4
from keymanager.operations.rsa_ssa_pkcs1_sha_operation import RsaSsaPkcs1Sha2562048KeyOperation
class Configuration:
    def __init__(
            self, credentials: Credential, retry_settings: RetrySettings, arx_url: str, arx_id: str) -> None:
        self._credentials = credentials
        self._arx_id = arx_id
        self._arx_url = arx_url
        self._retry_settings = retry_settings


class KeyManager:
    def __init__(self, option: Configuration ,random_service: CSPRNG) -> None:
        # hasher:
        self._hasher = Hasher()
        self._logger = logging.getLogger(self.__class__.__name__)
        self._index = "some value related to the arx url"
        self._config = {}
        self._http_client = Connection() # should pass all the params
        self._rsaSSAPKCS1KeyFactory = RSASSAPKCS1SHAKeyFactory(random_service=random_service)
        self._operations = {
            RsaSsapkcs12048sha256f4: RsaSsaPkcs1Sha2562048KeyOperation(self._rsaSSAPKCS1KeyFactory)
        }

    
    def fetch_encryption_key(self):
        raise NotImplementedError
    
    def fetch_decryption_key(self):
        raise NotImplementedError
    
    def unwrap_key(self):
        raise NotImplementedError