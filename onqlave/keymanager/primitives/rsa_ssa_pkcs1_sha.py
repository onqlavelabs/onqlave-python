from rsa import PrivateKey
from Crypto.IO import PEM
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from onqlave.keymanager.random_service import CSPRNG
from onqlave.errors.errors import (
    OnqlaveError,
    RSAImportKeyException,
    RSADecryptKeyException,
)
from onqlave.messages import messages


class RSASSAPKCS1SHA:
    def __init__(
        self,
        hash_function: any,
        hash_id,
        random_service: CSPRNG,
    ) -> None:
        self._random_service = random_service
        self._hash_function = hash_function
        self._hash_id = hash_id

    def unwrap_key(
        self,
        wdk: bytearray,
        epk: str,
        fp: bytearray,
        password: str,
    ) -> bytearray:
        try:
            private_key = RSA.import_key(epk, password)
        except Exception:
            raise RSAImportKeyException(
                message=messages.RSA_IMPORT_KEY_EXCEPTION,
                original_error=None,
                code=OnqlaveError.SdkErrorCode,
            )

        try:
            pkcs1_oaep = PKCS1_OAEP.new(
                key=private_key,
                hashAlgo=self._hash_function,
                randfunc=self._random_service.get_random_bytes,
            )
            data_key = pkcs1_oaep.decrypt(wdk)
        except Exception:
            raise RSADecryptKeyException(
                message=messages.RSA_DECRYPT_KEY_EXCEPTION,
                original_error=None,
                code=OnqlaveError.SdkErrorCode,
            )
        return data_key
