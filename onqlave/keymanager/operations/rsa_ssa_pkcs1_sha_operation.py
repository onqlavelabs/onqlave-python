from ctypes import c_uint32
from onqlave.keymanager.onqlave_types.types import HashType,HashTypeSHA256,KeyOperation, KeyFactory, KeyFormat
class RsaSsaPkcs1KeyFormat(KeyFormat):
    def __init__(self, version: c_uint32, hash: HashType) -> None:
        self._version = version
        self._hash = hash

    def get_hash(self):
        return self._hash
    

class RsaSsaPkcs1Sha2562048KeyOperation(KeyOperation):
    RsaSsaPkcs1KeyVersion = 0
    def __init__(self, factory: KeyFactory) -> None:
        self._factory = factory
        self._format = RsaSsaPkcs1KeyFormat(
            version=self.RsaSsaPkcs1KeyVersion,
            hash = HashTypeSHA256
        )

    def get_format(self) -> RsaSsaPkcs1KeyFormat:
        return self._format
    
    def get_factory(self):
        return self._factory