from onqlave.keymanager.onqlave_types.types import KeyFormat, KeyFactory, KeyOperation
from onqlave.keymanager.operations.aes_128_gcm_operation import (
    AesGcmKeyFormat,
    AESGCMKeyVersion,
)

AESGCM256KeySizeByteLength = 32


class Aes256GcmKeyOperation(KeyOperation):
    def __init__(self, key_factory: KeyFactory) -> None:
        self._format = AesGcmKeyFormat(
            key_size=AESGCM256KeySizeByteLength, version=AESGCMKeyVersion
        )
        self._factory = key_factory

    def get_format(self) -> KeyFormat:
        return self._format

    def get_factory(self) -> KeyFactory:
        return self._factory
