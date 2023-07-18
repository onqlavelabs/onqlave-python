

class OnqlaveError:
    """ The Error object for Onqlave APIs. Contains:
        1. Code - represents the type of the error
        2. Message - the message contained in the error
        3. originalError - the original error (if any) which resulted in this err
    """
    InvalidInput = "InvalidInput"
    SdkErrorCode = "400"
    Server = "Server"

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

class OnqlaveException(Exception):
    def __init__(
            self, 
            message: str, 
            original_error: any,
            code: str,
        ) -> None:
        self._message = message
        self._original_error = original_error
        self._code = code


    def get_message(self):
        return self._messsage
    
    def get_original_error(self) -> any:
        return self._original_error
    
    def get_code(self) -> any:
        return self._code

class InvalidCountTimeException(OnqlaveException):
    pass
        
class InvalidWaitTimeException(OnqlaveException):
    pass

class InvalidMaxWaitTimeException(OnqlaveException):
    pass


class FetchEncryptionKeyException(OnqlaveException):
    pass

class FetchDecryptionKeyException(OnqlaveException):
    pass

class UnmarshallKeyDataException(OnqlaveException):
    pass

class UnWrapKeyException(OnqlaveException):
    pass

class InvalidKeyException(OnqlaveException):
    pass

class InvalidPrimitiveException(OnqlaveException):
    pass

class OperationMappingException(OnqlaveException):
    pass

class CreatingKeyException(OnqlaveException):
    pass

class CreatingPrimitiveException(OnqlaveException):
    pass

class RSAImportKeyException(OnqlaveException):
    pass

class RSADecryptKeyException(OnqlaveException):
    pass



class ClientExctractingContentException(OnqlaveException):
    pass

class ClientCalculatingDigestException(OnqlaveException):
    pass

class ClientCalculatingSignatureException(OnqlaveException):
    pass


class EncryptionOperationException(OnqlaveException):
    pass

class PlainStreamWriteHeaderException(OnqlaveException):
    pass

class AlgorithmSerialisingException(OnqlaveException):
    pass

class InvalidCipherDataException(OnqlaveException):
    pass

