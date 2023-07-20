import sys
import base64
import io

from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

try:
    sys.path.remove(str(parent))
except ValueError: # Already removed
    pass

from onqlave.encryption import options
from onqlave.encryption.encryption import Encryption
from onqlave.credentials.credentials import Credential
from onqlave.connection.client import RetrySettings

# these data are generated when you create your api key in Onqlave Platform
# you should figure out an appropriate way to include them in your code as env variables
credentials = [
    {
        "access_key": "your access key",
        "arx_url": "your arx url",
        "server_signing_key": "your signing key",
        "server_secret_key": "your secret key",
        "client_key": ""
    },
]


debug_option = options.DebugOption(enable_debug=True) # toggle the debug option

# for example you want to try several encryption mechanisms, just make a for loop like this
# if you just want to stick with 1 encryption mechanisms, simply remove the loop
for each_cred in credentials:
    # init the configuration for the encryption service
    arx_option = options.ArxOption(arx_url=each_cred['arx_url'])
    credential_option = Credential(
        access_key=each_cred['access_key'],
        signing_key=each_cred['server_signing_key'],
        secret_key=each_cred['server_secret_key'])
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
    
    # encrypt/decrypt stream example
    plain_file_stream = open("path to your plaintext file","rb")
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
        "path to your decrypted file",
        "wb"
    ) as result:
        result.write(decrypted_stream.read())