from keymanager.id_service import IDService
from ctypes import c_uint32
from keymanager.random_service import CSPRNG
from onqlave_types.types import KeyOperation, Key, KeyFormat
from primitives.aes_gcm_aead import validate_aes_key_size
class AesGcmKeyFactory:
    def __init__(self) -> None:
        self._id_service = IDService()
        self._random_service = CSPRNG()
        # do something here to create new key ???

    def new_key(self,operation: KeyOperation):
        format = operation.get_format()

    
    def validate_key(self,key: Key):
        key_data = key.data()
        # validate key version

        # validate key value
        key_value = key_data.get_value()

        # validate aes key size
        key_size = len(key_value) # should caset to uint32
        validate_aes_key_size(key_size) # check this


    def validate_key_version(self,version: c_uint32, max_expected: c_uint32) -> bool:
        if version > max_expected:
            print("should return error")
            return False
        return True
    
    def validate_key_format(self, format: KeyFormat) -> bool:
        if not validate_aes_key_size(format.size()):
            return False
        return True