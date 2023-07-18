import base64
from datetime import datetime

# from onqlave.credentials.credentials import Credential
# from onqlave.connection.client import RetrySettings
from onqlave.utils.hasher import Hasher
from onqlave.logger.logger import OnqlaveLogger
from onqlave.contracts.requests.requests import (
    EncryptionOpenRequest,
    DecryptionOpenRequest,
)
from onqlave.connection.connection import Connection, Configuration
from onqlave.encryption.options import DebugOption
from onqlave.keymanager.factories.rsa_ssa_pkcs1_sha_factory import (
    RSASSAPKCS1SHAKeyFactory,
)
from onqlave.keymanager.random_service import CSPRNG
from onqlave.keymanager.onqlave_types.types import RsaSsapkcs12048sha256f4
from onqlave.keymanager.operations.rsa_ssa_pkcs1_sha_operation import (
    RsaSsaPkcs1Sha2562048KeyOperation,
)
from onqlave.messages import messages
from onqlave.errors.errors import (
    OnqlaveError,
    FetchEncryptionKeyException,
    FetchDecryptionKeyException,
    UnmarshallKeyDataException,
    UnWrapKeyException,
    OperationMappingException,
)


ENCRYPT_RESOURCE_URL = "oe2/keymanager/encrypt"
DECRYPT_RESOURCE_URL = "oe2/keymanager/decrypt"

# class Configuration:
#     def __init__(
#             self, credentials: Credential, retry_settings: RetrySettings, arx_url: str, arx_id: str) -> None:
#         self._credentials = credentials
#         self._arx_id = arx_id
#         self._arx_url = arx_url
#         self._retry_settings = retry_settings


class KeyManager:
    """A class for performing key handling operations at client slide, including:
    - Fetch encryption/decryption key
    - Unwrap the fetched encryption/decryption key
    """

    def __init__(
        self,
        configuration: Configuration,
        random_service: CSPRNG,
        debug_option: DebugOption,
    ) -> None:
        """Instantiates a key manager

        Args:
            configuration: the desired configuration to instantiate this key manager
            random_service: a random service that is going to be used by this key manager

        Returns:
            Nothing
        """
        # hasher:
        self._hasher = Hasher()
        self._logger = OnqlaveLogger(debug_option.get_debug_option())
        self._index = ""
        self._config = configuration
        self._http_client = Connection(
            configuration=self._config,
            hasher=self._hasher,
            logger=self._logger,
        )
        self._rsaSSAPKCS1KeyFactory = RSASSAPKCS1SHAKeyFactory(
            random_service=random_service
        )
        self._operations = {
            RsaSsapkcs12048sha256f4: RsaSsaPkcs1Sha2562048KeyOperation(
                self._rsaSSAPKCS1KeyFactory
            )
        }

    def fetch_encryption_key(self):
        """Fetch the encryption key from a defined Arx then parsing
        the data_key, wrapping_key, security_model from the response

        Args:
            Nothing

        Returns:
            A tuple contains:
            encrypted_data_key - edk: bytes
            data_key - dk
            algorithm

        """
        operation = "FetchEncryptionKey"
        start = datetime.utcnow()
        request = EncryptionOpenRequest(body_data={})
        self._logger.log_debug(
            messages.FETCHING_ENCRYPTION_KEY_OPERATION.format(operation)
        )

        data = self._http_client.post(resource=ENCRYPT_RESOURCE_URL, body=request)
        if data is None:
            raise FetchEncryptionKeyException(
                message=messages.FETCH_ENCRYPTION_KEY_EXCEPTION,
                original_error=None,
                code=OnqlaveError.SdkErrorCode,
            )

        try:
            edk = base64.b64decode(data["data_key"]["encrypted_data_key"])
            wdk = base64.b64decode(data["data_key"]["wrapped_data_key"])
            epk = base64.b64decode(
                data["wrapping_key"]["encrypted_private_key"]
            ).decode("ISO-8859-1")
            fp = base64.b64decode(data["wrapping_key"]["key_fingerprint"])
            wrapping_algorithm = data["security_model"]["wrapping_algo"]
            algorithm = data["security_model"]["algo"]
        except Exception:
            raise UnmarshallKeyDataException(
                message=messages.UNMARSHALL_KEY_DATA_EXCEPTION,
                original_error=None,
                code=OnqlaveError.SdkErrorCode,
            )

        dk = self.unwrap_key(
            wrapping_algorithm=wrapping_algorithm,
            operation=operation,
            wdk=wdk,
            epk=epk,
            fp=fp,
            password=self._config._credentials._secret_key,
        )

        finish = datetime.utcnow()
        self._logger.log_debug(
            messages.FETCHED_ENCRYPTION_KEY_OPERATION.format(
                operation,
                str(
                    f"{(finish-start).seconds} secs and {(finish-start).microseconds} microsecs"
                ),
            )
        )
        return edk, dk, algorithm

    def fetch_decryption_key(self, edk: bytearray):
        """Get the decryption key from the Onqlave Platform and parsing the received data

        Args:
            edk: the encrypted data key as a bytearray

        Returns
            dk: the unwrapped data key as a bytearray
        """
        operation = "FetchDecryptionKey"
        start = datetime.utcnow()

        request = DecryptionOpenRequest(
            body_data={"encrypted_data_key": base64.b64encode(edk).decode("utf-8")}
        )

        data = self._http_client.post(resource=DECRYPT_RESOURCE_URL, body=request)

        try:
            wdk = base64.b64decode(data["data_key"]["wrapped_data_key"])
            epk = base64.b64decode(
                data["wrapping_key"]["encrypted_private_key"]
            ).decode("ISO-8859-1")
            fp = base64.b64decode(data["wrapping_key"]["key_fingerprint"])
            wrapping_algorithm = data["security_model"]["wrapping_algo"]
        except Exception:
            raise UnmarshallKeyDataException(
                message=messages.UNMARSHALL_KEY_DATA_EXCEPTION,
                original_error=None,
                code=OnqlaveError.SdkErrorCode,
            )

        dk = self.unwrap_key(
            wrapping_algorithm=wrapping_algorithm,
            operation=operation,
            wdk=wdk,
            epk=epk,
            fp=fp,
            password=self._config._credentials._secret_key,
        )

        finish = datetime.utcnow()
        self._logger.log_debug(
            messages.FETCHED_DECRYPTION_OPERATION.format(
                operation,
                str(
                    f"{(finish-start).seconds} secs and {(finish-start).microseconds} microsecs"
                ),
            )
        )
        return dk

    def unwrap_key(
        self,
        wrapping_algorithm: str,
        operation: str,
        wdk: bytearray,
        epk: bytearray,
        fp: bytearray,
        password: bytearray,
    ):
        """Get the data key by unwrapping the fetched wrapped key

        Args:
            wrapping_algorithm: a string specified the used algo
            operation: a string specified the used operation
            wdk: a wrapped data key as bytearray
            epk: an encrypted private key as bytearray
            fp: finger print key as bytearray
            password: a secret used to encrypt the key, as bytearray

        Returns:
            The unwrapped data key
        """
        start = datetime.utcnow()

        wrapping_operation = self._operations[wrapping_algorithm]
        if wrapping_operation is None:
            raise OperationMappingException(
                message=messages.OPERATION_MAPPING_EXCEPTION,
                original_error=None,
                code=OnqlaveError.SdkErrorCode,
            )

        factory = wrapping_operation.get_factory()
        primitive = factory.primitive(wrapping_operation)

        dk = primitive.unwrap_key(wdk=wdk, epk=epk, fp=fp, password=password)

        finish = datetime.utcnow()
        self._logger.log_debug(
            "Key unwrap operation took {}".format(
                str(
                    f"{(finish-start).seconds} secs and {(finish-start).microseconds} microsecs"
                )
            )
        )
        if dk is None:
            raise UnWrapKeyException(
                message=messages.UNWRAP_KEY_EXCEPTION,
                original_error=None,
                code=OnqlaveError.SdkErrorCode,
            )

        return dk
