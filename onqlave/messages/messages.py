# This is a list of constants for log messages
SDK = "SDK"

FETCHING_ENCRYPTION_KEY_OPERATION = "[onqlave] SDK: {} - Fetching encryption key"
FETCHING_ENCRYPTION_KEY_RESPONSE_UNMARSHALING_FAILED = (
    "[onqlave] SDK: {} - Failed unmarshalling encryption key response"
)
FETCHED_ENCRYPTION_KEY_OPERATION = (
    "[onqlave] SDK: {} - Fetched encryption key: operation took {}"
)

FETCHING_DECRYPTION_OPERATION = "[onqlave] SDK: {} - Fetching decryption key"
FETCHING_DECRYPTION_KEY_RESPONSE_UNMARSHALING_FAILED = (
    "[onqlave] SDK: {} - Failed unmarshalling decryption key response"
)
FETCHED_DECRYPTION_OPERATION = (
    "[onqlave] SDK: {} - Fetched decryption key: operation took {}"
)

KEY_INVALID_WRAPPING_ALGO = "[onqlave] SDK: {} - Invalid wrapping algorithm"
KEY_INVALID_WRAPPING_OPERATION = "[onqlave] SDK: {} - Invalid wrapping operation"
KEY_UNWRAPPING_KEY_FAILED = "[onqlave] SDK: {} - Failed unwrapping encryption key"
KEY_INVALID_ENCRYPTION_OPERATION = "[onqlave] SDK: {} - Invalid encryption operation"
KEY_INVALID_DECRYPTION_OPERATION = "[onqlave] SDK: {} - Invalid encryption operation"

ENCRYPTING_OPERATION = "[onqlave] SDK: {} - Encrypting plain data"
ENCRYPTED_OPERATION = "[onqlave] SDK: {} - Encrypted plain data: operation took {}"
ENCRYPTION_OPERATION_FAILED = "[onqlave] SDK: {} - Failed encrypting plain data"

DECRYPTING_OPERATION = "[onqlave] SDK: {} - Decrypting cipher data"
DECRYPTED_OPERATION = "[onqlave] SDK: {} - Decrypted cipher data: operation took {}"
DECRYPTION_OPERATION_FAILED = "[onqlave] SDK: {} - Failed decrypting cipher data"

CLIENT_ERROR_EXTRACTING_CONTENT = (
    "[onqlave] SDK: {} - Failed extracting request content"
)
CLIENT_ERROR_CALCULATING_DIGEST = (
    "[onqlave] SDK: {} - Failed calculating request digest"
)
CLIENT_ERROR_CALCULATING_SIGNATURE = (
    "[onqlave] SDK: {} - Failed calculating request signature"
)
CLIENT_ERROR_PORTING_REQUEST = "[onqlave] SDK: {} - Failed sending {} request"

CLIENT_OPERATION_STARTED = "[onqlave] SDK: {} - Sending request started"
CLIENT_OPERATION_SUCCESS = (
    "[onqlave] SDK: {} - Sending request finished successfully: operation took {}"
)
HTTP_OPERATION_STARTED = "[onqlave] SDK: {} - Http operation started"
HTTP_OPERATION_SUCCESS = (
    "[onqlave] SDK: {} - Http operation finished successfully: operation took {}"
)
