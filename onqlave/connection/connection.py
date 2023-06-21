from credentials.credentials import Credential
from connection.client import RetrySettings,Client
from utils.hasher import Hasher


class Configuration:

    def __init__(
            self, 
            credentials: Credential,
            retry_settings: RetrySettings,
            arx_url: str,
            arx_id: str
    ) -> None:
        self._credentials = credentials # Credential type
        self._retry_settings = retry_settings # retry setting
        self._arx_url = arx_url
        self._arx_id = arx_id

    def get_retry_setting(self):
        return self._retry
    

class Connection:
    
    def __init__(
        self, 
        configuration: Configuration,
        hasher: Hasher,
        logger: any            
    ):
        self._retry_settings = configuration._retry_settings
        self._client = Client(self._retry_settings,logger)
        self._hasher = hasher
        self._logger = logger
        self._configuration = configuration

    # def post(self) -> None:
    #     pass
