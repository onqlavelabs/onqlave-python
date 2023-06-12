
class Hasher:
    def __init__(self) -> None:
        pass

    def digest(self, body_data) -> None:
        """hash the body_data using sha-512() then encode with base64
        """
        pass

    def sign(self,header_data, signing_key) -> None:
        """sign the header data with a signing key using hmac-sha512
        """
        pass