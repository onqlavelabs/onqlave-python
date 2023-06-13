class RetrySettings:
    def __init__(self, count: int, wait_time: int, max_wait_time: int) -> None:
        self._count = self._validate_and_get_count_value(count)
        self._wait_time = self._validate_and_get_count_value(wait_time)
        self._max_wait_time = self._validate_and_get_count_value(max_wait_time)

    def _validate_and_get_count_value(self, count: int) -> int:
        return count
    
    def _validate_and_get_wait_time_value(self, wait_time: int) -> int:
        return wait_time

    def _validate_and_get_max_wait_time_value(self, max_wait_time: int) -> int:
        return max_wait_time

class Client:

    def __init__(self) -> None:
        self._logger = None # init Onqlave logger here
        self._client = None # init a http client here
        self._retry_setting = None # init a retry setting instance here

    def post(self) -> None:
        pass

    def do_request_with_retry(self) -> None:
        pass
