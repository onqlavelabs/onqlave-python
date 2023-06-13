
class Encryption:
    """A class that models the encryption services with 2 main groups of features:
    - Encrypt/Decrypt data blocks
    - Encrypt/Decrypt data streams
    Before actually begin the encrypt/decrypt, it requires an init step for these operations
    """

    def __init__(self, key_manager, logger, operations) -> None:
        """ Init an instance of the encryption service with the following params:
        option = {credentials, retryoptions, arx_url}
        logger
        random_number_generation_service
        id_gen_service
        aead_gcm_key_factory
        x_ch_cha_key_factory 

        """
        self._key_mamanger = key_manager
        self._logger = logger
        self._operations = operations

    # impl setters & getters

    # init encrypt/decrypt operations
    def init_encrypt_operation(self) -> None:
        """Return the algorithm and primitives of the encrypt operation
        """
        # get the edk, dk, algo from Onqlave keymanager

        #
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
