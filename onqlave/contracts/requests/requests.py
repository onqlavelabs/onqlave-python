

class OnqlaveRequest:
    def get_content(): # return []byte, error
        raise NotImplementedError 
    
class EncryptionOpenRequest(OnqlaveRequest):
    def get_content():
        raise NotImplementedError # return json.marshal(r)

class DecryptionOpenRequest(OnqlaveRequest):
    def __init__(self) -> None:
        self._edk = "encrypted_data_key" # required, max = 1500
    
    def get_content():
        raise NotImplementedError # ...