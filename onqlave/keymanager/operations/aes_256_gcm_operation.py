from ctypes import c_uint32
from onqlave.keymanager.onqlave_types.types import KeyFormat, KeyFactory
from onqlave.keymanager.operations.aes_128_gcm_operation import AesGcmKeyFormat

class Aes256GcmKeyOperation:
    def __init__(self, key_factory: KeyFactory) -> None:
        self._format = AesGcmKeyFormat(key_size=32,version=0)
        self._factory = key_factory

    def get_format(self) -> KeyFormat:
        return self._format
    
    def get_factory(self) -> KeyFactory:
        return self._factory