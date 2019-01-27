import sys
import hashlib
import requests

url="https://api.pwnedpasswords.com/range/"
hash_object = hashlib.sha1(sys.argv[1].encode("UTF-8"))
pw_hash=hash_object.hexdigest()
first_part=pw_hash[:5]
second_part=pw_hash[5:]
print(pw_hash)
print(first_part)
print(second_part)
furl="{}{}".format(url,first_part)
print(furl)
response=requests.get(furl)
if second_part.lower() in response.text.lower():
    print("hash found")
