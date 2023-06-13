from .credentials import Credential
from ..connection.client import RetrySettings
class Configuration:
    def __init__(
            self, credentials: Credential, retry_settings: RetrySettings, arx_url: str, arx_id: str) -> None:
        self._credentials = credentials
        self._retry_settings = retry_settings
        self._arx_url = arx_url
        self._retry_settings = retry_settings

    
