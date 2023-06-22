from requests import Request

class OnqlaveRequest(Request):
    def __init__(self):
        super().__init__()
    
    def get_content(self): # return []byte, error
        pass
    
class EncryptionOpenRequest(OnqlaveRequest):
    pass
    def get_content(self):
        # raise NotImplementedError # return json.marshal(r)
        return super().get_content

class DecryptionOpenRequest(OnqlaveRequest):
    def __init__(self) -> None:
        self._edk = "encrypted_data_key" # required, max = 1500
        super().__init__()
    
    # def get_content(self):
    #     raise NotImplementedError # ...