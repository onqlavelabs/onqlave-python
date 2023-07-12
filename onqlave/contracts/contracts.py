
class EncryptionSecurityModel:
    def __init__(self,algo,wrapping_algo) -> None:
        self._algorithm = algo 
        self._wrapping_algorithm = wrapping_algo 


class WrappingKey:
    def __init__(self,epk,fp) -> None:
        self._epk = epk 
        self._key_fingerprint = fp 

class DataEncryptionKey:
    def __init__(self,edk,wdk) -> None:
        self._edk = edk 
        self._wdk = wdk 

class DataDecryptionKey:
    def __init__(self, wdk) -> None:
        self._wdk = wdk