
from keymanager.onqlave_types.types import Key
from keymanager.random_service import CSPRNG
class AESGCMAEAD:
    def __init__(
            self, 
            key: Key, 
            random_service: CSPRNG
    ) -> None:
        self._random_service = random_service
        self._key_value = key.data().get_value()
        if not validate_aes_key_size(len(self._key_value)):
            raise Exception # should be detailed
        
        self.prependIV = True
        


def validate_aes_key_size(size_in_bytes: int) -> bool:
    if size_in_bytes in [16,32]:
        return True
    return False