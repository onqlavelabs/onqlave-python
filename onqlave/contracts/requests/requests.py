import json

from onqlave.errors.errors import OnqlaveError, ClientExctractingContentException
from onqlave.messages import messages


class OnqlaveRequest:
    def __init__(self, body_data: dict):
        self._json = body_data

    def get_content(self):
        try:
            result = json.dumps(self._json)
        except Exception:
            raise ClientExctractingContentException(
                message=messages.CLIENT_ERROR_EXTRACTING_CONTENT,
                original_error=None,
                code=OnqlaveError.SdkErrorCode,
            )
        return result


class EncryptionOpenRequest(OnqlaveRequest):
    def __init__(self, body_data: dict):
        super().__init__(body_data=body_data)


class DecryptionOpenRequest(OnqlaveRequest):
    def __init__(self, body_data: dict) -> None:
        super().__init__(body_data=body_data)
