import hmac
from hashlib import sha512
import base64

ServerType        = "Onqlave/0.1"
Version           = "0.1"
Oonqlave_Content  = "application/json"

OnqlaveAPIKey         = "ONQLAVE-API-KEY"
OnqlaveContent        = "Content-Type"
OnqlaveHost           = "ONQLAVE-HOST"
OnqlaveVersion        = "ONQLAVE-VERSION"
OnqlaveSignature      = "ONQLAVE-SIGNATURE"
OnqlaveDigest         = "ONQLAVE-DIGEST"
OnqlaveArx            = "ONQLAVE-ARX"
OnqlaveAgent          = "User-Agent"
OnqlaveRequestTime    = "ONQLAVE-REQUEST-TIME"
OnqlaveContentLength  = "ONQLAVE-CONTEXT-LEN"

headers_to_sign = {
    OnqlaveAPIKey: "onq.jlhnKpD73UAbBPj2XuD86BMmtSeLvW16",
    OnqlaveArx: "cluster--RhiaE00keTpDEE9phzUid",
    OnqlaveHost: "https://dp0.onqlave.io",
    OnqlaveAgent: ServerType,
    OnqlaveContentLength: "2",
    OnqlaveDigest: "SHA512=J8dGcK23UHX60FjVzq97IMTneGyDuuijL2Jvl4KvNMmjPCBG72D9Knh403jin+yFGAa72aZ4ePOp8c2kgwdj/Q==",
    OnqlaveVersion: Version,
}

header_keys = sorted([header for header,value in headers_to_sign.items()])

signing_key = "onq.1GrQGFAKXdgU0iMPFuXKh6sjCIeNBkdE"
# msg = ''.join([f"{k.lower()}:{headers_to_sign[k].lower()}" for k in header_keys]).encode('utf-8')

signature = hmac.new(signing_key.encode('utf-8'),None,sha512)

for header_name in header_keys:
    input_str = f"{header_name.lower()}:{headers_to_sign[header_name]}"
    signature.update(input_str.encode('utf-8'))

digest = signature.digest()


print(f"HMAC-SHA512={str(base64.b64encode(digest).decode())}")