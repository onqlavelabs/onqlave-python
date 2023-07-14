import hmac
import base64
from hashlib import sha512

from onqlave.contracts.requests.requests import OnqlaveRequest
class Hasher:
    def __init__(self) -> None:
        pass

    def digest(self, body_data: OnqlaveRequest) -> None:
        """hash the body_data using sha-512() then encode with base64
        """
        hashing_function = sha512()
        hashing_function.update(body_data.get_content().encode('utf-8'))
        digest = hashing_function.digest()
        return f"SHA512={base64.b64encode(digest).decode()}"

    def sign(self,header_data:dict, signing_key) -> None:
        """pre process + sign the header data with a signing key using hmac-sha512
        """
        header_names = sorted([header_name for header_name,value in header_data.items()])
        signing_function = hmac.new(signing_key.encode('utf-8'),None,sha512)
        
        for header_name in header_names:
            input_str = f"{header_name.lower()}:{header_data[header_name]}"
            signing_function.update(input_str.encode('utf-8'))

        digest = signing_function.digest()
        return f"HMAC-SHA512={str(base64.b64encode(digest).decode())}"
