
class EncryptionSecurityModel:
    def __init__(self,algo,wrapping_algo) -> None:
        self._algorithm = algo # "algo"
        self._wrapping_algorithm = wrapping_algo # "wrapping_algo"


class WrappingKey:
    def __init__(self,epk,fp) -> None:
        self._epk = epk # "encrypted_private_key"
        self._key_fingerprint = fp # "key_fingerprint"

class DataEncryptionKey:
    def __init__(self,edk,wdk) -> None:
        self._edk = edk # "encrypted_data_key"
        self._wdk = wdk # "wrapped_data_key"

class DataDecryptionKey:
    def __init__(self, wdk) -> None:
        self._wdk = wdk # "wrapped_data_key"