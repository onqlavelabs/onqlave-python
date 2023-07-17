from ctypes import c_uint32
from onqlave.keymanager.onqlave_types.types import KeyFactory,KeyFormat, KeyOperation

XchaCha20Poly1305KeyVersion = 0

class XChaChaKeyFormat(KeyFormat):
    def __init__(self,key_size: c_uint32, version: c_uint32) -> None:
        self._key_size = key_size
        self._version = version

    def size(self) -> c_uint32:
        return self._key_size

class XChaCha20Poly1305KeyOperation(KeyOperation):
    def __init__(self, key_factory: KeyFactory) -> None:
        self._factory = key_factory
        self._format = XChaChaKeyFormat(32,XchaCha20Poly1305KeyVersion)

    def get_format(self):
        return self._format
    
    def get_factory(self):
        return self._factory