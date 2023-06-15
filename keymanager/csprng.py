from ctypes import c_uint32

class CSPRNG:
    def __init__() -> None:
        pass

    def get_random_bytes(self, size: int) -> None:
        raise NotImplementedError

    def get_random_uint32(self) -> c_uint32:
        raise NotImplementedError

    def get_random_reader() -> any:
        raise NotImplementedError