class Credential:
    def __init__(self, access_key: str, signing_key: str, secret_key: str) -> None:
        self._access_key = self._validate_key(access_key)
        self._signing_key = self._validate_key(signing_key)
        self._secret_key = self._validate_key(secret_key)

    def _validate_key(self, key: str) -> str | None:
        return None if key == "" else key
            
