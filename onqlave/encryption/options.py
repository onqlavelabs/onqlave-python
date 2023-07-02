class DebugOption:
    """A class modeling the configuration of the debug mode
    """
    def __init__(self, enable_debug: bool) -> None:
        self._debug = enable_debug
    
    def get_debug_option(self) -> bool:
        return self._debug if self._debug is not None else False
    
    def set_debug_option(self, enable_debug: bool) -> None:
        self._debug = enable_debug


class ArxOption:
    """A class for modeling the configuration of the Arx-related params in the encryption/decryption request
    """
    def __init__(self, arx_url: str) -> None:
        self._arx_url = self._check_url(arx_url)
        
    def _check_url(self,url: str) -> str:
        return url

    def set_arx_url(self,url:str) -> None:
        self._arx_url = self._check_url(url)

    def get_arx_url(self) -> str:
        return self._arx_url
    


