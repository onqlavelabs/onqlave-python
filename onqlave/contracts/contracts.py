
class EncryptionSecurityModel:
    def __init__(self) -> None:
        self._algorithm = "algo"
        self._wrapping_algorithm = "wrapping_algo"


class WrappingKey:
    def __init__(self) -> None:
        self._epk = "encrypted_private_key"
        self._key_fingerprint = "key_fingerprint"

class DataEncryptionKey:
    def __init__(self) -> None:
        self._edk = "encrypted_data_key"
        self._wdk = "wrapped_data_key"

class DataDecryptionKey:
    def __init__(self) -> None:
        self._wdk = "wrapped_data_key"