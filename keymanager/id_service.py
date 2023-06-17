from ctypes import c_uint32
class IDService:
    def __init__() -> None:
        pass

    def new_string_id() -> str:
        raise NotImplementedError

    def new_key_id() -> c_uint32:
        raise NotImplementedError