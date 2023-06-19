from ctypes import c_uint32
from keymanager.onqlave_types.types import KeyFactory
from keymanager.factories.aes_gcm_factory import AEADGCMKeyFactory
AESGCMKeyVersion = 0

class AesGcmKeyFormat:
    def __init__(self, key_size: c_uint32, version: c_uint32) -> None:
        self._key_size = key_size
        self._key_version = version
    
    def size(self) -> c_uint32:
        return self._key_size

class AesGcmKeyOperation:
    def __init__(self,key_factory: AEADGCMKeyFactory) -> None:
        self._factory = key_factory
        self._format = AesGcmKeyFormat(key_size=16,version=AESGCMKeyVersion) # need to change this

    