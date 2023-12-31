
import io
from onqlave.encryption import options
from onqlave.encryption.encryption import Encryption
from onqlave.credentials.credentials import Credential
from onqlave.connection.client import RetrySettings


# This example demonstrates how to use Onqlave python sdk with credentials loaded from a JSON file
debug_option = options.DebugOption(enable_debug=True) # toggle the debug option

# init the configuration for the encryption service by loading from a json file
cred_file_path = "credentials.json"

arx_option = options.ArxOption()
credential_option = Credential()

arx_option.load_arx_url_from_json(cred_file_path)
credential_option.load_config_from_json(cred_file_path)

retry_option = RetrySettings(count=1,wait_time=1,max_wait_time=2) # retry when server fails

encryption_engine = Encryption( # init an encryption service
        debug_option=debug_option,
        arx_option=arx_option,
        credential_option=credential_option,
        retry_setting=retry_option
    )

    # encrypt/decrypt example
plaintext = "hello world" # your data goes here
associated_data = "auth" # your authentication data goes here
cipher_text = encryption_engine.encrypt(plaintext.encode(), associated_data.encode())
decrypted_cipher = encryption_engine.decrypt(cipher_text,associated_data.encode())
if not decrypted_cipher.decode() == plaintext:
    print("Encrypt/decrypt FAILED")
    raise Exception # encrypt/decrypt FAILED
print("Encrypt/decrypt OK")
    # encrypt/decrypt stream example
plain_file_stream = open("plaintext.txt","rb")
plain_stream = io.BytesIO(plain_file_stream.read())
cipher_stream = io.BytesIO()
    
encryption_engine.encrypt_stream(plain_stream,cipher_stream,associated_data.encode())
cipher_stream.seek(0) # rewind your pointer to the beginning position

decrypted_stream = io.BytesIO()
encryption_engine.decrypt_stream(
        cipher_stream=cipher_stream,
        plain_stream=decrypted_stream,
        associated_data=associated_data.encode()
)
decrypted_stream.seek(0)

with open(
        "decrypted.txt",
        "wb"
) as result:
    result.write(decrypted_stream.read())

plaintext_in_stream = None
decrypted_text_in_stream = None
with open("decrypted.txt","r") as f:
    decrypted_text_in_stream = f.readline()
with open("plaintext.txt","r") as f:
    plaintext_in_stream = f.readline()

if not plaintext_in_stream == decrypted_text_in_stream:
    print("Encrypt/decrypt stream FAILED")
    raise Exception # encrypt/decrypt stream FAILED
print("Encrypt/decrypt stream OK")