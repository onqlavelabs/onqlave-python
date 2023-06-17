from ctypes import c_uint32
from ..onqlave_types.types import KeyFormat, KeyFactory
from .aes128_gcm_operation import AesGcmKeyFormat

class Aes256GcmKeyOperation:
    def __init__(self, factory: KeyFactory) -> None:
        self._format = AesGcmKeyFormat()
        self._factory = KeyFactory(factory)

    def get_format(self) -> KeyFormat:
        return self._format
    
    def get_factory(self) -> KeyFactory:
        return self._factory