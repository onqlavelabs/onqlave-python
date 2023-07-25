
import io
import os
import argparse
from onqlave.encryption import options
from onqlave.encryption.encryption import Encryption
from onqlave.credentials.credentials import Credential
from onqlave.connection.client import RetrySettings


# This example demonstrates how to use Onqlave python sdk with credentials loaded from CLI args
def main():
    parser = argparse.ArgumentParser(
        "Python SDK",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("-ak", "--access_key", help="access_key", type=str)
    parser.add_argument("-au", "--arx_url", help="arx_url", type=str)
    parser.add_argument("-ssk", "--server_signing_key", help="server_signing_key", type=str)
    parser.add_argument("-ssek", "--server_secret_key", help="server_secret_key", type=str)

    args = parser.parse_args()
    access_key = args.access_key
    arx_url = args.arx_url
    server_signing_key = args.server_signing_key
    server_secret_key = args.server_secret_key

    debug_option = options.DebugOption(enable_debug=True) # toggle the debug option

    # init the configuration for the encryption service
    arx_option = options.ArxOption(arx_url=arx_url)
    credential_option = Credential(
            access_key=access_key,
            signing_key=server_signing_key,
            secret_key=server_secret_key
        )
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
            "path to your decrypted file",
            "wb"
    ) as result:
        result.write(decrypted_stream.read())

if __name__ == '__main__':
    main()