from ..random_service import CSPRNG
from ctypes import c_int32
from onqlave_types.types import HashTypeName
from hashlib import sha1,sha224,sha256,sha384,sha512

class RSASSAPKCS1SHAKeyFactory:
    def __init__(self, random_service: CSPRNG) -> None:
        self._random_service = random_service
    
    def rsa_hash_func(self, hash_algorithm: str) :
        """Return a hash function with a hash algorithm ID"""
        hash_function = self._get_hash_function(hash_algorithm)
        if hash_function is None:
            raise ValueError()
        
        hash_id = self._get_hash_id(hash_algorithm)
        if hash_id == 0:
            raise ValueError()
        
        return hash_function,hash_id
    
    def primitive(self) -> None:
        raise NotImplementedError
    
    def _get_hash_function(self, hash: str) -> any:
        if hash == "SHA1":
            return sha1
        elif hash == "SHA224":
            return sha224
        elif hash == "SHA256":
            return sha256
        elif hash == "SHA384":
            return sha384
        elif hash == "SHA512":
            return sha512
        else:
            return None

    def _get_hash_type(self, hash_type: c_int32) -> str:
        return HashTypeName[hash_type]
    
    def _get_hash_id(self,hash_algorithm: str) -> int:
        if hash_algorithm == "SHA256":
            return 5
        elif hash_algorithm == "SHA384":
            return 6
        elif hash_algorithm == "SHA512":
            return 7
        else:
            return 0

    def _is_hash_safe_for_signature(self, hash_algorithm: str) -> bool:
        if hash_algorithm in ["SHA256","SHA384","SHA512"]:
            return True
        return False
    