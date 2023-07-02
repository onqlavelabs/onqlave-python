import secrets

from ctypes import c_uint32

class CSPRNG:
    """A class that instantiates cryptographically secured pseudo-random number generators
    """
    def __init__(self) -> None:
        """Nothing much about this standard init method
        
        Args:
            Nothing

        Returns:
            Nothing
        """
        pass

    def get_random_bytes(self, size: int) -> bytes:
        """Get a random bytes from the built-in libraries of Python
        
        Args:
            size: an integer describes the size of the randomized bytes

        Returns:
            Randomized bytes
        """
        return secrets.token_bytes(nbytes=size)
        

    def get_random_uint32(self) -> c_uint32:
        """Get a random unsigned 32-bit integer 

        Args:
            Nothing

        Returns:
            A randomized unsigned 32-bit integer
        """
        return int.from_bytes(self.get_random_bytes(4),byteorder='big')

    def get_random_reader(self) -> any:
        raise NotImplementedError