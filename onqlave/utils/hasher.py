import hmac
import base64
from hashlib import sha512
class Hasher:
    def __init__(self) -> None:
        pass

    def digest(self, body_data) -> None:
        """hash the body_data using sha-512() then encode with base64
        """
        digest_hash = sha512()
        # digest_hash.update(body_data)
        # digest_hash.digest()
        print("hashing the body content here ....")
        pass

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
