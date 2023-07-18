from ctypes import c_uint32
from onqlave.keymanager.onqlave_types.types import KeyFactory, KeyFormat, KeyOperation

AESGCMKeyVersion = 0
AESGCM128KeySizeByteLength = 16


class AesGcmKeyFormat:
    def __init__(self, key_size: c_uint32, version: c_uint32) -> None:
        self._key_size = key_size
        self._key_version = version

    def size(self) -> c_uint32:
        return self._key_size


class AesGcmKeyOperation(KeyOperation):
    def __init__(self, key_factory: KeyFactory) -> None:
        self._factory = key_factory
        self._format = AesGcmKeyFormat(
            key_size=AESGCM128KeySizeByteLength, version=AESGCMKeyVersion
        )

    def get_format(self) -> KeyFormat:
        return self._format

    def get_factory(self) -> KeyFactory:
        return self._factory
