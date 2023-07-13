import logging
import requests
import time 
import urllib.request
import json 
import http.client

from datetime import datetime

from contracts.requests.requests import OnqlaveRequest
from logger.logger import OnqlaveLogger

from messages import messages
class RetrySettings:
    """A class for initializing the retry setting, default value is:
    - count = 3
    - wait_time = 400ms
    - max_wait_time = 2000ms
    """
    def __init__(
            self, 
            count: int = 3, 
            wait_time: int = 400, 
            max_wait_time: int = 2000
    ) -> None:
        self._count = self._validate_and_get_count_value(count)
        self._wait_time = self._validate_and_get_count_value(wait_time)
        self._max_wait_time = self._validate_and_get_count_value(max_wait_time)

    def _validate_and_get_count_value(self, count: int) -> int:
        if count <= 0:
            raise Exception # invalid count time
        return count
    
    def _validate_and_get_wait_time_value(self, wait_time: int) -> int:
        if wait_time <=0:
            raise Exception # invalid wait time
        return wait_time

    def _validate_and_get_max_wait_time_value(self, max_wait_time: int) -> int:
        if max_wait_time < 0:
            raise Exception # invalid max wait time
        return max_wait_time 

class Client:
    """A wrapper for the http client with the retry settings as an additional feature
    """
    def __init__(
            self, 
            retry_setting: RetrySettings,
            logger: OnqlaveLogger, 
    ) -> None:
        self._logger = logger
        self._retry_setting = retry_setting

    def post(
            self, 
            resource: str, 
            request_body: OnqlaveRequest,
            headers: dict        
    ):
        """Send the body data to the resource URL

        Args:
            resource: a part of the resource url
            request_body: the request body object
            headers: a dict contains the http headers

        Return:
            The jsonified response
        """
        operation = "Http"
        self._logger.log_debug(messages.HTTP_OPERATION_STARTED.format(operation))
        start = datetime.utcnow()
        
        json_body = request_body._json

        start_request = datetime.utcnow()
        request = urllib.request.Request(url=resource, headers=headers, data=json.dumps(json_body).encode('utf-8'))
        start_request = datetime.utcnow()
        response = urllib.request.urlopen(request)
        response_data = response.read().decode('utf-8')
        result = json.loads(response_data)
        finish_request = datetime.utcnow()
        self._logger.log_debug("sending request... done {} {}".format(operation,str(f'{(finish_request-start_request).seconds} secs and {(finish_request-start_request).microseconds} microsecs')))

        if response.status == 500:
            try:
                response = self.do_request_with_retry(resource=resource,headers=headers, body=json_body)
            except Exception as exc:
                raise exc
        if response.status == 429:
            raise Exception # return onqlaveerrors.SDKerrorcode
        elif response.status >= 400:
            raise Exception
        
        finish = datetime.utcnow()
        self._logger.log_debug(messages.HTTP_OPERATION_SUCCESS.format(operation,str(f'{(finish-start).seconds} secs and {(finish-start).microseconds} microsecs')))
        return result
        
    def do_request_with_retry(
            self, 
            resource: str,
            headers: dict,
            body) -> None:
        """Send request with the specified retry setting to handle the case of server errors
        Args:
            resource: a part of the resource url
            body: the body data of the http request (as dict)

        Returns:
            The response
        """
        response = requests.Response()
        for i in range(0,self._retry_setting._count):
            response = requests.post(url=resource,headers=headers,body=body)
            if response.status_code < 500:
                return response
            time.sleep(self._retry_setting._max_wait_time)

        return response

