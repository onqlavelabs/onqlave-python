from ctypes import c_uint32

from onqlave.keymanager.onqlave_types.types import KeyID
from onqlave.keymanager.random_service import CSPRNG
class IDService:
    """A class defining the ID generation service
    """
    def __init__(self, random_service: CSPRNG) -> None:
        """Init the ID service by feeding a random service into it

        Args:
            random_service: a random service defined in the same module

        Returns:
            Nothing
        """
        self._random_service = random_service

    def new_string_id(self) -> str:
        raise NotImplementedError

    def new_key_id(self) -> KeyID:
        """Get a new random key id
        
        Args:
            Nothing
        
        Returns:
            Nothing
        """
        return KeyID(self._random_service.get_random_uint32())