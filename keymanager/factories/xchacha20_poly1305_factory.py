from ctypes import c_uint32

from ..id_service import IDService
from ..random_service import CSPRNG
from ..onqlave_types.types import KeyOperation,Key,KeyFormat

class XChaCha20Poly1305KeyFactory:
    def __init__(self) -> None:
        self._id_service = IDService()
        self._random_service = CSPRNG()

    def new_key(self, operation: KeyOperation):
        raise NotImplementedError
    
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