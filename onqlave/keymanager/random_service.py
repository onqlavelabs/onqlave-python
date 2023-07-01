import secrets

from ctypes import c_uint32

class CSPRNG:
    def __init__(self) -> None:
        pass

    def get_random_bytes(self, size: int) -> bytes:
        return secrets.token_bytes(nbytes=size)
        

    def get_random_uint32(self) -> c_uint32:
        return int.from_bytes(self.get_random_bytes(4),byteorder='big')

    def get_random_reader(self) -> any:
        
        raise NotImplementedError