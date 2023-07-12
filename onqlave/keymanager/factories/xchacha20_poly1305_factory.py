from ctypes import c_uint32

from keymanager.onqlave_types.types import Key, KeyOperation, KeyMaterialSYMMETRIC
from keymanager.keys.xchacha_20_poly_1350 import XChaCha20Poly1305KeyData, XChaCha20Poly1305Key
from keymanager.primitives.xchacha20_poly1305_aead import XChaCha20Poly1305AEAD
from ..id_service import IDService
from ..random_service import CSPRNG
from ..onqlave_types.types import KeyOperation,Key,KeyFormat,KeyFactory

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
                value=key_data,
                key_material_type=KeyMaterialSYMMETRIC,
                version=0
            )
        )
    
    def primitive(self, key: Key):
        # validate the key
        ret = XChaCha20Poly1305AEAD(
            key=key,
            random_service=self._random_service
        )
        return ret
    
    def validate_key(self, key: Key):
        # validate key version
    
        # validate key value

        # validate xchacha key size
        raise NotImplementedError
    
    def validate_key_format(self, format: KeyFormat):
        self.validate_xchacha_key_size(format.size())
        
    
    def validate_xchacha_key_size(self, size_int_byte: int):
        if size_int_byte != ChaCha20Poly1305KeySize:
            raise Exception # invalid xchacha key size
        

    
    def validate_key_version(self, version: c_uint32, max_expected: c_uint32) -> bool:
        if version > max_expected:
            return False
        return True
    
    def validate_key_size(self, size_in_bytes: c_uint32) -> bool:
        if size_in_bytes != 32: # need to double check this because golang SDK use constant from other lib
            return False
        return True