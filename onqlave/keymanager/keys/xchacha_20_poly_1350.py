from keymanager.onqlave_types.types import KeyMaterialType, KeyID, KeyOperation

class XChaCha20Poly1305KeyData:
    """A class define the blueprint of XChaCha20Poly1305 key data
    """
    def __init__(
            self,
            # type_url: str,
            value: bytearray,
            key_material_type: KeyMaterialType,
            version: int
    ) -> None:
        # self._type_url = type_url
        self._version = version
        self._value = value
        self._key_material_type = key_material_type
        
    def get_value(self):
        return self._value
        
    def get_key_material_type(self):
        return self._key_material_type
    
    def get_version(self):
        return self._version

class XChaCha20Poly1305Key:
    def __init__(
            self,
            key_id: KeyID,
            operation: KeyOperation,
            data: XChaCha20Poly1305KeyData
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