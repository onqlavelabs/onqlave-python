import calendar
from datetime import datetime

from credentials.credentials import Credential
from connection.client import RetrySettings,Client
from contracts.requests.requests import OnqlaveRequest
from utils.hasher import Hasher

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

    def post(self,resource: str, body: OnqlaveRequest) -> None:
        operation = "Post"
        start = datetime.utcnow()
        # log the operation
        url_string = self._configuration._arx_url + "/" + resource
        arx_id = self._configuration._arx_id

        digest = self._hasher.digest(body)

        headers_to_sign = {
            OnqlaveAPIKey: self._configuration._credentials._access_key,
            OnqlaveArx: arx_id,
            OnqlaveHost: self._configuration._arx_url,
            OnqlaveAgent: ServerType,
            OnqlaveContentLength: str(len(body.get_content())),
            OnqlaveDigest: digest,
            OnqlaveVersion: Version
        }
        # add try-catch
        signature = self._hasher.sign(headers_to_sign,self._configuration._credentials._signing_key)
        
        headers = {
            OnqlaveContent: Oonqlave_Content,
            OnqlaveAPIKey: self._configuration._credentials._access_key,
            OnqlaveArx: arx_id,
            OnqlaveHost: self._configuration._arx_url,
            OnqlaveAgent: ServerType,
            OnqlaveRequestTime:str(calendar.timegm(datetime.utcnow().timetuple())),
            OnqlaveContentLength: str(len(body.get_content())),
            OnqlaveDigest: digest,
            OnqlaveVersion: Version,
            OnqlaveSignature: signature
        }
        response = self._client.post(url_string,request_body=body, headers=headers)
        return response # need to handle errors later

# {
# 	"access_key": "onq.JlnL5YDsC8O6NperEMNdf0DM7vaYHhl5",
# 	"arx_url": "https://gcp.community.serverless.au.dp0.onqlave.com/cluster--Qludg9OeHwhtGGbd8LSPB",
# 	"server_signing_key": "onq.GZDANwPQ2VY2XzfaxEq7eq9mfPoUjHKv",
# 	"server_secret_key": "onq.26j0WfMlQnPUYGdcyceq6a1raJd8JacJKltWe6Towlox91zlGiupL7FtdYUl0Rr6PKl3e3gS7oYU3364Wt8r4Q9KRD4zwSMuCQI9aJbsptPGYTnnBOURjjORPpVSsake",
# 	"client_key": ""
# }