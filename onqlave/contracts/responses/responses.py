from ctypes import c_uint

from onqlave.contracts.contracts import WrappingKey,EncryptionSecurityModel,DataDecryptionKey,DataEncryptionKey

class BaseErrorResponse:
    def __init__(self) -> None:
        self._error = "error"

class Error:
    def __init__(
            self, 
            status: str, 
            message: str, 
            correlation_id: str, 
            details: any, 
            code: int
    ) -> None:
        self._status = status
        self._message = message
        self._correlation_id = correlation_id
        self._details = details
        self._code = code

class DecryptionOpenResponse:
    def __init__(
            self,
            wrapping_key: WrappingKey, 
            security_model: EncryptionSecurityModel,
            data_key: DataDecryptionKey
    ) -> None:
        self._wk = wrapping_key
        self._security_model = security_model
        self._dk = data_key
        self._error_response = None

class EncryptionOpenResponse:
    def __init__(
            self,
            wrapping_key: WrappingKey,
            data_key: DataEncryptionKey,
            security_model: EncryptionSecurityModel,
            max_uses: c_uint
    ) -> None:
        self._wk = wrapping_key
        self._dk = data_key
        self._security_model = security_model
        self._max_uses = max_uses
        self._error_response = None

    