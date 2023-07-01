from keymanager.onqlave_types.types import KeyMaterialType, KeyID

class XChaCha20Poly1305KeyData:
    def __init__(
            self,
            type_url: str,
            value: bytearray,
            key_material_type: KeyMaterialType
    ) -> None:
        self._type_url = type_url
        self._value = value
        self._key_material_type = key_material_type

    