
class Configuration:
    def __init__(self) -> None:
        self._credential = None # Credential type
        self._retry = None # retry setting
        self._arx_url = None
        self._arx_id = None


class Credential:
    def __init__(self) -> None:
        self._access_key = None
        self._signing_key = None


class Connection:
    
    def __init__(self) -> None:
        self._client = None
        self._hasher = None
        self._logger = None
        self._configuration = None

    def post(self) -> None:
        pass

