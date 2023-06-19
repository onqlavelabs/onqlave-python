
class OnqlaveError:
    """ The Error object for Onqlave APIs. Contains:
        1. Code - represents the type of the error
        2. Message - the message contained in the error
        3. originalError - the original error (if any) which resulted in this err
    """

    def __init__(self) -> None:
        self._originalError=None
        self._code=None
        self._message=None

    # getters
    def get_original_error(self) -> any:
        return self._originalError
    
    def get_code(self) -> any:
        return self._code
    
    def get_message(self) -> any:
        return self._message