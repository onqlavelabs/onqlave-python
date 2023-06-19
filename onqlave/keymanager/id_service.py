from ctypes import c_uint32
class IDService:
    def __init__(self) -> None:
        pass

    def new_string_id(self) -> str:
        raise NotImplementedError

    def new_key_id(self) -> c_uint32:
        raise NotImplementedError