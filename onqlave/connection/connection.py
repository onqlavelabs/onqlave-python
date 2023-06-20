from credentials.credentials import Credential
from client import RetrySettings,Client
from utils.hasher import Hasher
class Configuration:
    def __init__(
            self, 
            credential: Credential,
            retry_setting: RetrySettings,
            arx_url: str,
            arx_id: str
    ) -> None:
        self._credential = credential # Credential type
        self._retry = retry_setting # retry setting
        self._arx_url = arx_url
        self._arx_id = arx_id


class Connection:
    
    def __init__(
        self, 
        configuration: Configuration,
        hasher: Hasher,
        logger: any            
    ) -> None:
        self._client = Client(configuration._retry,logger)
        self._hasher = hasher
        self._logger = logger
        self._configuration = configuration

    # def post(self) -> None:
    #     pass

