import calendar
from datetime import datetime

from onqlave.credentials.credentials import Credential
from onqlave.connection.client import RetrySettings,Client
from onqlave.contracts.requests.requests import OnqlaveRequest
from onqlave.logger.logger import OnqlaveLogger
from onqlave.messages import messages
from onqlave.utils.hasher import Hasher

# A list of header constants
OnqlaveAPIKey         = "ONQLAVE-API-KEY"
OnqlaveContent        = "Content-Type"
OnqlaveHost           = "ONQLAVE-HOST"
OnqlaveVersion        = "ONQLAVE-VERSION"
OnqlaveSignature      = "ONQLAVE-SIGNATURE"
OnqlaveDigest         = "ONQLAVE-DIGEST"
OnqlaveArx            = "ONQLAVE-ARX"
OnqlaveAgent          = "User-Agent"
OnqlaveRequestTime    = "ONQLAVE-REQUEST-TIME"
OnqlaveContentLength  = "ONQLAVE-CONTEXT-LEN"

ServerType        = "Onqlave/0.1"
Version           = "0.1"
Oonqlave_Content  = "application/json"

class Configuration:
    """Init an object to store the configuration information
    """
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
        logger: OnqlaveLogger            
    ):
        self._retry_settings = configuration._retry_settings
        self._client = Client(self._retry_settings,logger)
        self._hasher = hasher
        self._logger = logger
        self._configuration = configuration

    def post(self, resource: str, body: OnqlaveRequest) -> None:
        """Send a request to the Onqlave Platform to fetch the neccessary data for the encryption process
        """
        operation = "Post"
        start = datetime.utcnow()
        
        self._logger.log_debug(messages.CLIENT_OPERATION_STARTED.format(operation))
        
        url_string = self._configuration._arx_url + "/" + resource
        arx_id = self._configuration._arx_id

        
        content = body.get_content()

        digest = self._hasher.digest(body)

        headers_to_sign = {
            OnqlaveAPIKey: self._configuration._credentials._access_key,
            OnqlaveArx: arx_id,
            OnqlaveHost: self._configuration._arx_url,
            OnqlaveAgent: ServerType,
            OnqlaveContentLength: str(len(content)),
            OnqlaveDigest: digest,
            OnqlaveVersion: Version
        }
        
        signature = self._hasher.sign(headers_to_sign,self._configuration._credentials._signing_key)
        
        headers = {
            OnqlaveContent: Oonqlave_Content,
            OnqlaveAPIKey: self._configuration._credentials._access_key,
            OnqlaveArx: arx_id,
            OnqlaveHost: self._configuration._arx_url,
            OnqlaveAgent: ServerType,
            OnqlaveRequestTime:str(calendar.timegm(datetime.utcnow().timetuple())),
            OnqlaveContentLength: str(len(content)),
            OnqlaveDigest: digest,
            OnqlaveVersion: Version,
            OnqlaveSignature: signature
        }
        response = self._client.post(url_string,request_body=body, headers=headers)
        finish = datetime.utcnow()
        self._logger.log_debug(messages.CLIENT_OPERATION_SUCCESS.format(operation,str(f'{(finish-start).seconds} secs and {(finish-start).microseconds} microsecs')))
        return response