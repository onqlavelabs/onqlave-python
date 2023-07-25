import json
import os

class Credential:
    """Modeling the configurations of the credentials used in the initialisation of the encrypt/decrypt operation
    """
    def __init__(self, access_key: str="", signing_key: str="", secret_key: str="") -> None:
        """Init the Credential object with three values of access_key, signing_key, secret_key,
        these values are packed in the response from the Onqlave platform
        Args:
            access_key: str
            signing_key: str
            secret_key: str

        Returns:
            Nothing
        """
        self._access_key = self._validate_key(access_key)
        self._signing_key = self._validate_key(signing_key)
        self._secret_key = self._validate_key(secret_key)

    def _validate_key(self, key: str) -> str:
        return None if key == "" else key
    
    def load_config_from_json(self, json_file_path: str):
        if not os.path.exists(json_file_path):
            raise FileNotFoundError
        with open(json_file_path,"r") as f:
            credentials = json.load(f)
            self._access_key = credentials['access_key']
            self._signing_key = credentials['server_signing_key']
            self._secret_key = credentials['server_secret_key']

            