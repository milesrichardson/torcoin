import hashlib
import base64
from ecdsa import SigningKey, VerifyingKey

message = 'VENBVFRFTVBUOjE6YTFkMGM2ZTgzZjAyNzMyN2Q4NDYxMDYzZjRhYzU4YTY6YzRjYTQyMzhhMGI5MjM4MjBkY2M1MDlhNmY3NTg0OWI6YzgxZTcyOGQ5ZDRjMmY2MzZmMDY3Zjg5Y2MxNDg2MmM6ZWNjYmM4N2U0YjVjZTJmZTI4MzA4ZmQ5ZjJhN2JhZjM6j1Q39D43q/Rien7H85+c9dkWwaudlMNL3M/c1hNx0AMwGcEaMsIPk6LjdTriGlZFOjM='
message = base64.b64decode(message)
message_split = message.split(":")
for i in message_split:
  print("-"+i+"-")
# assert message_split[2] == hashlib.md5(message_split[13]).hexdigest()
assert message_split[3] == hashlib.md5(message_split[11]).hexdigest()
assert message_split[4] == hashlib.md5(message_split[9]).hexdigest()
assert message_split[5] == hashlib.md5(message_split[7]).hexdigest()
vk1 = VerifyingKey.from_pem(open('operations/1.pem', 'r').read())
vk2 = VerifyingKey.from_pem(open('operations/2.pem', 'r').read())
vk3 = VerifyingKey.from_pem(open('operations/3.pem', 'r').read())
B = message_split[0] + ":" + message_split[1] + ":" + message_split[2] + \
    ":" + message_split[3] + ":" + message_split[4] + ":" + message_split[5]
assert vk1.verify(message_split[10], B)
assert vk2.verify(message_split[8], B)
assert vk3.verify(message_split[6], B)