from ctypes import c_uint32

class AESGCMAEAD:
    def __init__(self) -> None:
        self._random_service
        self._key
        self.prependIV


def validate_aes_key_size(size_in_bytes: c_uint32) -> bool:
    if size_in_bytes in [16,32]:
        return True
    return False