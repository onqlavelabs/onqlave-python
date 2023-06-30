import logging
import base64
from datetime import datetime

# from credentials.credentials import Credential
# from connection.client import RetrySettings
from utils.hasher import Hasher
# from logger.logger import OnqlaveLogging
from contracts.requests.requests import EncryptionOpenRequest
from connection.connection import Connection,Configuration
from keymanager.factories.rsa_ssa_pkcs1_sha_factory import RSASSAPKCS1SHAKeyFactory
from keymanager.random_service import CSPRNG
from keymanager.onqlave_types.types import RsaSsapkcs12048sha256f4
from keymanager.operations.rsa_ssa_pkcs1_sha_operation import RsaSsaPkcs1Sha2562048KeyOperation
from errors.errors import OnqlaveError


ENCRYPT_RESOURCE_URL  = "oe2/keymanager/encrypt"
DECRYPT_RESOURCE_URL  = "oe2/keymanager/decrypt"

# class Configuration:
#     def __init__(
#             self, credentials: Credential, retry_settings: RetrySettings, arx_url: str, arx_id: str) -> None:
#         self._credentials = credentials
#         self._arx_id = arx_id
#         self._arx_url = arx_url
#         self._retry_settings = retry_settings


class KeyManager:
    def __init__(self, configuration: Configuration ,random_service: CSPRNG) -> None:
        # hasher:
        self._hasher = Hasher()
        self._logger = logging.getLogger(self.__class__.__name__)
        self._index = "some value related to the arx url"
        self._config = configuration
        self._http_client = Connection(
            configuration=self._config,
            # configuration=configuration,
            hasher=self._hasher,
            logger=self._logger
        ) # should pass all the params
        self._rsaSSAPKCS1KeyFactory = RSASSAPKCS1SHAKeyFactory(random_service=random_service)
        self._operations = {
            RsaSsapkcs12048sha256f4: RsaSsaPkcs1Sha2562048KeyOperation(self._rsaSSAPKCS1KeyFactory)
        }

    
    def fetch_encryption_key(self):
        operation  = "FetchEncryptionKey"
        start = datetime.utcnow()
        request = EncryptionOpenRequest(body_data={})
        # log debug with message = fetching encryption key operation
        data = self._http_client.post(resource=ENCRYPT_RESOURCE_URL,body=request)
        # validate data
        # these thing needs to be replaced with onqlave response object
        edk = base64.b64decode(data['data_key']['encrypted_data_key']).decode('ISO-8859-1')
        wdk = base64.b64decode(data['data_key']['wrapped_data_key']).decode('ISO-8859-1')
        epk = base64.b64decode(data['wrapping_key']['encrypted_private_key']).decode('ISO-8859-1')
        fp = base64.b64decode(data['wrapping_key']['key_fingerprint']).decode('ISO-8859-1')
        wrapping_algorithm = data['security_model']['wrapping_algo']
        algorithm = data['security_model']['algo']
        
        # unwrap the key
        dk = self.unwrap_key(
            wrapping_algorithm=wrapping_algorithm,
            operation=operation,
            wdk=wdk,
            epk=epk,
            fp=fp,
            password=bytearray(self._config._credentials._secret_key,'utf-8')
        )
        #get the response
        print(f"hooray, dk = {dk}")
        # decode data including: edk, wdk, epk, fp
        return (edk,dk,algorithm,OnqlaveError())
    
    def fetch_decryption_key(self):
        operation  = "FetchDecryptionKey"
        raise NotImplementedError
    
    def unwrap_key(
            self, 
            wrapping_algorithm: str, 
            operation: str, 
            wdk: bytearray, 
            epk: bytearray,
            fp: bytearray,
            password: bytearray
    ):
        wrapping_operation = self._operations[wrapping_algorithm]
        if wrapping_operation is None:
            return None
        factory = wrapping_operation.get_factory()
        primitive = factory.primitive(wrapping_operation)
        # check if primitive assignment had some errors
        dk = primitive.unwrap_key(
            wdk=wdk,epk=epk,fp=fp,password=password
        )
        return dk
        

