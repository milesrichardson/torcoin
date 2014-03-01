import sys
import hashlib

argc = len(sys.argv)
if not (3 <= argc <= 4):
  print "Usage: TCGenerate Position <Received Hash> Key"
  exit(-1)

position = sys.argv[1]
# print "Position: " + position

if position != "0":
  received_hash = sys.argv[2]
  hash_attempt = sys.argv[3]
else:
  received_hash = ""
  hash_attempt = sys.argv[2]

# print "Received Hash: " + received_hash
# print "hash attempt: " + hash_attempt

m = hashlib.md5(received_hash + hash_attempt)
print m.hexdigest()

# The next part of the code will be in the server
import StoreHash
StoreHash.storeInHashTable("1", m.hexdigest())