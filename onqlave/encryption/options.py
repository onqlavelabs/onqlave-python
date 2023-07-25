import os
import json
import logging 

class DebugOption:
    """A class modeling the configuration of the debug mode for the Onqlave logger
    """
    def __init__(self, enable_debug: bool) -> None:
        self._debug = enable_debug
    
    def get_debug_option(self) -> bool:
        """Get the debug option status

        Args:
            Nothing

        Returns:
            The status of the debug option as a bool value
        """
        return logging.DEBUG if self._debug else logging.INFO
    
    def set_debug_option(self, enable_debug: bool) -> None:
        """Enable/disable the debug option
        
        Args:
            enable_debug: a bool value

        Returns:
            Nothing
        """
        self._debug = enable_debug


class ArxOption:
    """A class for modeling the configuration of the Arx-related params in the encryption/decryption request
    """
    def __init__(self, arx_url: str="") -> None:
        self._arx_url = arx_url

    def set_arx_url(self,url:str) -> None:
        self._arx_url = self._check_url(url)

    def get_arx_url(self) -> str:
        return self._arx_url
    
    def load_arx_url_from_json(self, json_file_path: str):
        if not os.path.exists(json_file_path):
            raise FileNotFoundError
        with open(json_file_path,"r") as f:
            credentials = json.load(f)
            self._arx_url = credentials['arx_url']


