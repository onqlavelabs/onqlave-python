from hashlib import sha1,sha224,sha256,sha384,sha512
from onqlave.keymanager.random_service import CSPRNG
from ctypes import c_int32
from onqlave.keymanager.onqlave_types.types import HashTypeName,KeyFactory
from onqlave.keymanager.onqlave_types.types import AEAD, Key,KeyOperation
from onqlave.keymanager.operations.rsa_ssa_pkcs1_sha_operation import RsaSsaPkcs1Sha2562048KeyOperation
from onqlave.keymanager.primitives.rsa_ssa_pkcs1_sha import RSASSAPKCS1SHA
from Crypto.Hash import SHA1,SHA224,SHA256,SHA384,SHA512

from onqlave.keymanager.onqlave_types.types import Key, KeyOperation
class RSASSAPKCS1SHAKeyFactory(KeyFactory):
    """Modelling the RSA-SSA-PKCS1-SHA Key factory
    """
    def __init__(self, random_service: CSPRNG) -> None:
        self._random_service = random_service

    def new_key_from_data(operation: KeyOperation, key_data: bytearray) -> Key:
        """Create new key from data

        Args:
            operation: an instance of KeyOperation
            key_data: a bytearray contains the key data

        Returns:
            A Key object
        """
        return super().new_key_from_data(key_data)
    
    def rsa_hash_func(self, hash_algorithm: str) :
        """Return a hash function with a hash algorithm ID

        Args:
            hash_algorithm: a string specifies the hash algorithm

        Returns:
            Nothing
        """
        hash_function = self._get_hash_function(hash_algorithm)
        if hash_function is None:
            raise ValueError()
        
        hash_id = self._get_hash_id(hash_algorithm)
        if hash_id == 0:
            raise ValueError()
        
        return hash_function,hash_id
    
    def _get_hash_function(self, hash: str) -> any:
        """Get the object specifies the selected hash function

        Args:
            hash:  a string as the name of the selected hash function

        Returns:
            The object that modelling the hash function or None
        """
        if hash == "SHA1":
            return SHA1
        elif hash == "SHA224":
            return SHA224
        elif hash == "SHA256":
            return SHA256
        elif hash == "SHA384":
            return SHA384
        elif hash == "SHA512":
            return SHA512
        else:
            return None

    def _get_hash_type(self, hash_type: c_int32) -> str:
        """Mapping the hash type from  int -> str
        
        Args:
            hash_type: an int
        
        Returns:
            The corresponding string as the name of the hash
        """
        return HashTypeName[hash_type.value]
    
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
    
    def primitive(self, operation:RsaSsaPkcs1Sha2562048KeyOperation) -> RSASSAPKCS1SHA:
        format = operation.get_format()

        try:
            hash_func, hash_id = self.rsa_hash_func(
                self._get_hash_type(format.get_hash())
            )
        except Exception as exc:
            raise exc # invalid hash config
        
        try:
            ret = RSASSAPKCS1SHA(
                hash_function=hash_func,
                hash_id=hash_id,
                random_service=self._random_service
            )
        except Exception as exc:
            raise exc # invalid primitive data
        
        return ret
        
    
    
    