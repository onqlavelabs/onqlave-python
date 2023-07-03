import logging
import requests
import time 
from datetime import datetime
from contracts.requests.requests import OnqlaveRequest
from messages import messages
class RetrySettings:
    def __init__(
            self, 
            count: int, 
            wait_time: int, 
            max_wait_time: int
    ) -> None:
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
    def __init__(
            self, 
            retry_setting: RetrySettings,
            logger: any, 
    ) -> None:
        self._logger = logging.getLogger() # init Onqlave logger here
        # self._client = requests # init a http client here
        self._retry_setting = retry_setting # init a retry setting instance here

    def post(
            self, 
            resource: str, 
            request_body: OnqlaveRequest,
            headers: dict        
    ): # return a byte array & error
        """Send the body data to the resource URL
        """
        operation = "Http"
        self._logger.debug(messages.HTTP_OPERATION_STARTED,operation,exc_info=1)
        start = datetime.utcnow()
        json_body = request_body._json
        response = requests.post(
            url=resource,
            headers=headers,
            json=json_body
        )
        # do something to retry the request
        if response.status_code == 429:
            raise Exception # return onqlaveerrors.SDKerrorcode
        elif response.status_code >= 400:
            raise Exception
        print(f"response = {response}")
        return response.json()
        
    def do_request_with_retry(self,resource,body) -> None:
        response = requests.Response()
        for i in range(0,self._retry_setting._count):
            response = requests.post(url=""+resource,body=body)
            if response.status_code < 500:
                return response
            time.sleep(self._retry_setting._max_wait_time)

        return response # should also return the error

