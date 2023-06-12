
class Client:

    def __init__(self) -> None:
        self._logger = None # init Onqlave logger here
        self._client = None # init a http client here
        self._retry_setting = None # init a retry setting instance here

    def post(self) -> None:
        pass

    def do_request_with_retry(self) -> None:
        pass
