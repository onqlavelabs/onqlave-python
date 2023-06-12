
class Encryption:

    def __init__(self, key_manager, logger, operations) -> None:
        self._key_mamanger = key_manager
        self._logger = logger
        self._operations = operations

    # impl setters & getters

    # init encrypt/decrypt operations
    def init_encrypt_operation(self) -> None:
        pass

    def init_decrypt_operation(self) -> None:
        pass

    # encrypt/decrypt
    def encrypt(self) -> None:
        pass

    def derypt(self) -> None:
        pass

    # encrypt/decrypt stream
    def encrypt_stream(self) -> None:
        pass

    def derypt_stream(self) -> None:
        pass

    # encrypt/decrypts structure
    def encrypt_structure(self) -> None:
        pass

    def derypt_structure(self) -> None:
        pass


