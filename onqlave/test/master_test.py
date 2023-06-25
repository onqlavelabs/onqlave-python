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

debug_option = options.DebugOption(enable_debug=True)
assert debug_option.get_debug_option() == True

arx_option = options.ArxOption(arx_url="https://dp0.onqlave.io/cluster--RhiaE00keTpDEE9phzUid")
assert type(arx_option.get_arx_url()) == str

credential_option = Credential(
    access_key="onq.Dwt6GE8wEBpMAu2ORAjYQntNM53hxw8O",
    signing_key="onq.mRjihyxeG5LyIMrE7xAPasiSfogR6CRv",
    secret_key="onq.mJZcj1CIZ5TOtrSZXY6OQUeUcfnx5FO84SLzecdlh2Pt8eIvc7PgKf4YLIEfxeaLPGrsCmcDQacW7lyvtjme3vFvmTCwOMUpdoPhCz5McINi4YNrQG1eisique5jJXP9")
retry_option = RetrySettings(count=1,wait_time=1,max_wait_time=2)

encryption_engine = Encryption(
    debug_option=debug_option,
    arx_option=arx_option,
    credential_option=credential_option,
    retry_setting=retry_option
)

encryption_engine.encrypt()
print("Hello Onqlave")