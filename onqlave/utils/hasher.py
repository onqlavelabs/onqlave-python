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
        """sign the header data with a signing key using hmac-sha512
        lowercase all the header data before signing
        """
        header_names = []
        for header_name, header_value in header_data.items():
            header_names.append(header_name)

        header_names = sorted(header_names)
        signing_key_as_byte_array = bytearray()
        signing_key_as_byte_array.extend(map(ord,signing_key))
        signature_hash = hmac.new(key=signing_key_as_byte_array,digestmod=sha512)
        for header_name in header_names:
            signature_hash.digest()

        print("signing something here....")
        pass