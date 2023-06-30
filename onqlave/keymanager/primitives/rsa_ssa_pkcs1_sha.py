from rsa import PrivateKey
from Crypto.IO import PEM

from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import rsa,padding
from cryptography.hazmat.backends import default_backend
from keymanager.random_service import CSPRNG
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
        epk: bytearray,
        fp: bytearray,
        password: bytearray
    ) -> bytearray:
        # private_key = PrivateKey()
        block, rem, operation_performed = PEM.decode(epk)
        if len(rem) != 0:
            private_key = load_pem_private_key(
                block,
                password=password
            )
            dk = private_key.decrypt(
            wdk,
            padding.OAEP(
                mgf=padding.MGF1(
                    algorithm=self._hash_function),
                algorithm=self._hash_function,
                label=None
            ))
            return dk
        
        else:
            print("wrapping key format error")
            return None
        # if no error happens
        

        