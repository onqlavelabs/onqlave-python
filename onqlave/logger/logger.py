import logging

class OnqlaveLogger:
    def __init__(self,level: int) -> None:
        self._logger = logging.getLogger("Onqlave-SDK")
        logging.basicConfig()
        self._logger.setLevel(level)
        
    def log_info(self, message):
        self._logger.info(message)

    def log_debug(self, message):
        self._logger.debug(message)

    def log_error(self, message):
        self._logger.error(message)

    def log_critical(self, message):
        self._logger.critical(message)
        