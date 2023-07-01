from rsa import PrivateKey
from Crypto.IO import PEM 
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

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
        epk: str,
        fp: bytearray,
        password: str,
    ) -> bytearray:
        private_key = RSA.import_key(epk,password)
        pkcs1_oaep = PKCS1_OAEP.new(
            key=private_key,
            hashAlgo=self._hash_function,
            randfunc=self._random_service.get_random_bytes
        )
        data_key = pkcs1_oaep.decrypt(wdk)
        print(data_key)
        return data_key
        # if no error happens
        

        