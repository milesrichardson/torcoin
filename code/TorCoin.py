import sys
import hashlib

def tc_generate(position, hash_attempt, received_hash = ""):
  '''
    Usage: tc_generate(position, hash_attempt, Received_Hash)
  '''
  # print "Received Hash: " + received_hash
  # print "hash attempt: " + hash_attempt
  m = hashlib.md5(str(received_hash) + str(hash_attempt))
  # print m.hexdigest()
  return m.hexdigest()

def tc_verify(position, stored_hash, *args):
  '''
    Usage: tc_verify(position,  Stored_Hash, Received_Key1, Received_Hash1...)
  '''
  argc = len(args)
  prev = stored_hash
  for i in xrange(0, argc-1, 2):
    m = hashlib.md5()
    # print str(i)
    m.update( str(prev) + str(args[i]))
    # print "HexD: " + m.hexdigest()
    if m.hexdigest() != args[i+1]:
      return False
    prev = m.hexdigest()
  return True

# The next part of the code will be in the server
# import StoreHash
# StoreHash.storeInHashTable("1", m.hexdigest())
