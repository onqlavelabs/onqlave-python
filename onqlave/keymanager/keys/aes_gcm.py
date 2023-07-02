from keymanager.onqlave_types.types import KeyOperation, KeyMaterialType, KeyID


class AesGcmKeyData:
    """A class defines the blueprint for the AES (GCM mode) key data
    """
    def __init__(
            self, 
            value: bytearray, 
            key_material_type: KeyMaterialType, 
            version: int
    ) -> None:
        self._type_url = None
        self._value = value
        self._key_material_type = key_material_type
        self._version = version

    def from_value(self):
        return None
    
    def get_value(self):
        return self._value
    
    def get_type_url(self):
        return self._type_url
    
    def get_key_material_type(self):
        return self._key_material_type
    
    def get_version(self):
        return self._version


class AesGcmKey:
    """A class defines the blueprint for the AES (GCM mode) key
    """
    def __init__(
            self, 
            operation: KeyOperation, 
            data: AesGcmKeyData,
            key_id: KeyID
    ) -> None:
        self._operation = operation
        self._data = data
        self._key_id = key_id

    def key_id(self):
        return self._key_id
    
    def operation(self):
        return self._operation
    
    def data(self):
        return self._data
        