from ctypes import c_uint32

from keymanager.onqlave_types.types import Key, KeyOperation

from ..id_service import IDService
from ..random_service import CSPRNG
from ..onqlave_types.types import KeyOperation,Key,KeyFormat,KeyFactory

class XChaCha20Poly1305KeyFactory(KeyFactory):
    def __init__(self, id_service: IDService, random_service: CSPRNG) -> None:
        self._id_service = id_service
        self._random_service = random_service

    def new_key(self, operation: KeyOperation):
        raise NotImplementedError

    def new_key_from_data(operation: KeyOperation, key_data: bytearray) -> Key:
        return super().new_key_from_data(key_data)
    
    def primitive(key: Key):
        raise NotImplementedError
    
    def validate_key(self, key: Key):
        # validate key version

        # validate key value

        # validate xchacha key size

        raise NotImplementedError
    
    def validate_key_format(format: KeyFormat):
        raise NotImplementedError
    
    def validate_key_version(version: c_uint32, max_expected: c_uint32) -> bool:
        if version > max_expected:
            return False
        return True
    
    def validate_key_size(size_in_bytes: c_uint32) -> bool:
        if size_in_bytes != 32: # need to double check this because golang SDK use constant from other lib
            return False
        return True