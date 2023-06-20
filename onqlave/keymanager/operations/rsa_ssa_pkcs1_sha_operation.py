from ctypes import c_uint32
from keymanager.onqlave_types.types import HashType,HashTypeSHA256,KeyOperation

class RsaSsaPkcs1KeyFormat:
    def __init__(self, version: c_uint32, hash: HashType) -> None:
        self._version = version
        self._hash = hash

class RsaSsaPkcs1Sha2562048KeyOperation(KeyOperation):
    RsaSsaPkcs1KeyVersion = 0
    def __init__(self, factory: any,) -> None:
        self._factory = factory
        self._format = RsaSsaPkcs1KeyFormat(
            version=self.RsaSsaPkcs1KeyVersion,
            hash = HashTypeSHA256
        )

    def get_format(self):
        return self._format
    
    def get_factory(self):
        return self._factory