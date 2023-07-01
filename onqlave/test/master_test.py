import sys
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

# Additionally remove the current file's directory from sys.path
try:
    sys.path.remove(str(parent))
except ValueError: # Already removed
    pass

from encryption import options
from encryption.encryption import Encryption
from credentials.credentials import Credential
from connection.client import RetrySettings

# {
# 	"access_key": "onq.Na557t4YmAnhYC2ddRXGd7s8AzRNNsoG",
# 	"arx_url": "https://dp0.onqlave.com/cluster--Qludg9OeHwhtGGbd8LSPB",
# 	"server_signing_key": "onq.QHwZKmLaMor2rY8yX6b21EIAvwCOzhkY",
# 	"server_secret_key": "onq.1neBvCfZXMeVdbsNcUZmEun1VkWOERkfppFGjljo344Wofa4fugeGh9P93uJo3npG5V6xd0hKY0yuOH8K0AnmTZUmYK8pBwypDVSApZnXzRsKcRXTQmJUkJTxx4KLy5c",
# 	"client_key": ""
# }

debug_option = options.DebugOption(enable_debug=True)
assert debug_option.get_debug_option() == True

arx_option = options.ArxOption(arx_url="https://dp0.onqlave.com/cluster--Qludg9OeHwhtGGbd8LSPB")
assert type(arx_option.get_arx_url()) == str

credential_option = Credential(
    access_key="onq.Na557t4YmAnhYC2ddRXGd7s8AzRNNsoG",
    signing_key="onq.QHwZKmLaMor2rY8yX6b21EIAvwCOzhkY",
    secret_key="onq.1neBvCfZXMeVdbsNcUZmEun1VkWOERkfppFGjljo344Wofa4fugeGh9P93uJo3npG5V6xd0hKY0yuOH8K0AnmTZUmYK8pBwypDVSApZnXzRsKcRXTQmJUkJTxx4KLy5c")
retry_option = RetrySettings(count=1,wait_time=1,max_wait_time=2)

encryption_engine = Encryption(
    debug_option=debug_option,
    arx_option=arx_option,
    credential_option=credential_option,
    retry_setting=retry_option
)

encryption_engine.encrypt()
print("Hello Onqlave")