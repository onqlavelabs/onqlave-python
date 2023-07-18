from ctypes import c_uint32

from onqlave.keymanager.onqlave_types.types import (
    Key,
    KeyOperation,
    KeyMaterialSYMMETRIC,
)
from onqlave.keymanager.keys.xchacha_20_poly_1350 import (
    XChaCha20Poly1305KeyData,
    XChaCha20Poly1305Key,
)
from onqlave.keymanager.primitives.xchacha20_poly1305_aead import XChaCha20Poly1305AEAD
from onqlave.keymanager.operations.xchacha20_poly1305_operation import (
    XchaCha20Poly1305KeyVersion,
)
from onqlave.keymanager.id_service import IDService
from onqlave.keymanager.random_service import CSPRNG
from onqlave.keymanager.onqlave_types.types import (
    KeyOperation,
    Key,
    KeyFormat,
    KeyFactory,
)
from onqlave.errors.errors import OnqlaveError, InvalidKeyException
from onqlave.messages import messages

ChaCha20Poly1305KeySize = 32


class XChaCha20Poly1305KeyFactory(KeyFactory):
    def __init__(self, id_service: IDService, random_service: CSPRNG) -> None:
        self._id_service = id_service
        self._random_service = random_service

    def new_key_from_data(self, operation: KeyOperation, key_data: bytearray) -> Key:
        format = operation.get_format()
        self.validate_key_format(format)
        return XChaCha20Poly1305Key(
            key_id=self._id_service.new_key_id(),
            operation=operation,
            data=XChaCha20Poly1305KeyData(
                value=key_data, key_material_type=KeyMaterialSYMMETRIC, version=0
            ),
        )

    def primitive(self, key: XChaCha20Poly1305Key):
        self.validate_key(key)
        ret = XChaCha20Poly1305AEAD(key=key, random_service=self._random_service)
        return ret

    def validate_key(self, key: XChaCha20Poly1305Key):
        if not self.validate_key_version(
            key.data().get_version(), XchaCha20Poly1305KeyVersion
        ):
            raise InvalidKeyException(
                message=messages.INVALID_KEY_EXCEPTION,
                original_error=None,
                code=OnqlaveError.SdkErrorCode,
            )

        key_value = key.data().get_value()
        
        if not self.validate_xchacha_key_size(len(key_value)):
            raise InvalidKeyException(
                message=messages.INVALID_KEY_EXCEPTION,
                original_error=None,
                code=OnqlaveError.SdkErrorCode,
            )

    def validate_key_format(self, format: KeyFormat):
        self.validate_xchacha_key_size(format.size())

    def validate_xchacha_key_size(self, size_int_byte: int):
        if size_int_byte != ChaCha20Poly1305KeySize:
            return False
        return True

    def validate_key_version(self, version: c_uint32, max_expected: c_uint32) -> bool:
        if version > max_expected:
            return False
        return True
