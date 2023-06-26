import json

from requests import Request

class OnqlaveRequest():
    def __init__(self,body_data: dict):
        self._json = body_data
    
    def get_content(self): # return []byte, error
        """convert to JSON encoding"""
        return json.dumps(self._json)
    
class EncryptionOpenRequest(OnqlaveRequest):
    def __init__(self,body_data: dict):
        super().__init__(body_data=body_data)
        
    def get_content(self):
        # raise NotImplementedError # return json.marshal(r)
        return json.dumps(self._json)
        

class DecryptionOpenRequest(OnqlaveRequest):
    def __init__(self) -> None:
        self._edk = "encrypted_data_key" # required, max = 1500
        super().__init__()
    
    # def get_content(self):
    #     raise NotImplementedError # ...