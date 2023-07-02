from ctypes import c_uint32

from keymanager.onqlave_types.types import KeyID
from keymanager.random_service import CSPRNG
class IDService:
    def __init__(self, random_service: CSPRNG) -> None:
        self._random_service = random_service

    def new_string_id(self) -> str:
        raise NotImplementedError

    def new_key_id(self) -> KeyID:
        return KeyID(self._random_service.get_random_uint32())