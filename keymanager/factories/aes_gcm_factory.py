from id_generator import IDService
from ctypes import c_uint32
from csprng import CSPRNG
from onqlave_types.types import KeyOperation, Key, KeyFormat
from primitives.aes_gcm_aead import validate_aes_key_size
class AesGcmKeyFactory:
    def __init__(self) -> None:
        self._id_service = IDService()
        self._random_service = CSPRNG()

    def new_key(self,operation: KeyOperation):
        format = operation.get_format()

    
    def validate_key(self,key: Key):
        key_data = key.data()

    def validate_key_version(self,version: c_uint32, max_expected: c_uint32) -> bool:
        if version > max_expected:
            print("should return error")
            return False
        return True
    
    def validate_key_format(self, format: KeyFormat) -> bool:
        if not validate_aes_key_size(format.size()):
            return False
        return True