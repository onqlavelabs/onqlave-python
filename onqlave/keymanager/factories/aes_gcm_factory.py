from onqlave.keymanager.id_service import IDService
from ctypes import c_uint32
from onqlave.keymanager.random_service import CSPRNG
from onqlave.keymanager.onqlave_types.types import KeyOperation, Key, KeyFormat, KeyFactory
from onqlave.keymanager.primitives.aes_gcm_aead import validate_aes_key_size, AESGCMAEAD
from onqlave.keymanager.keys.aes_gcm import AesGcmKey,AesGcmKeyData
from onqlave.keymanager.id_service import IDService
from onqlave.keymanager.onqlave_types.types import Key, KeyOperation, KeyMaterialSYMMETRIC
from onqlave.keymanager.onqlave_types.types import Key
from onqlave.keymanager.operations.aes_128_gcm_operation import AESGCMKeyVersion
from onqlave.errors.errors import OnqlaveError, InvalidKeyException, InvalidPrimitiveException
from onqlave.messages import messages

class AEADGCMKeyFactory(KeyFactory):
    """A class to init instances Key factory for the AEADGCM encryption process
    """
    def __init__(self, id_service: IDService, random_service: CSPRNG) -> None:
        self._id_service = id_service
        self._random_service = random_service


    def new_key_from_data(self, operation: KeyOperation, key_data: bytearray) -> Key:
        format = operation.get_format()
        if not self.validate_key_format(format):
            raise InvalidKeyException(
                message=messages.INVALID_KEY_EXCEPTION,
                original_error=None,
                code=OnqlaveError.SdkErrorCode
            )
        return AesGcmKey(
            key_id=self._id_service.new_key_id(),
            operation=operation,
            data=AesGcmKeyData(
                value=key_data,
                key_material_type=KeyMaterialSYMMETRIC,
                version=0
            )
        )
    
    def validate_key(self,key: Key):
        key_data = key.data()
        # validate key version
        if not self.validate_key_version(key_data.get_version(),AESGCMKeyVersion):
            return False
        # validate key value
        key_value = key_data.get_value()
        if key_value is None:
            return False
        # validate aes key size
        key_size = len(key_value)
        if not validate_aes_key_size(key_size):
            return False        
        return True


    def validate_key_version(self,version: c_uint32, max_expected: c_uint32) -> bool:
        if version > max_expected:
            return False
        return True
    
    def validate_key_format(self, format: KeyFormat) -> bool:
        if not validate_aes_key_size(format.size()):
            return False
        return True
    
    def primitive(self, key: Key) -> any:
        if not self.validate_key(key):
            raise InvalidPrimitiveException(
                message=messages.CREATING_PRIMITIVE_EXCEPTION,
                original_error=None,
                code=OnqlaveError.SdkErrorCode
            )
        try:
            ret = AESGCMAEAD(key=key,random_service=self._random_service)
        except Exception:
            raise InvalidPrimitiveException(
                message=messages.CREATING_PRIMITIVE_EXCEPTION,
                original_error=None,
                code=OnqlaveError.SdkErrorCode
            )
        return ret
        