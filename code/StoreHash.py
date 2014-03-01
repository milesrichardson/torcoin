# Once a hash is generated, it is stored in a hash table indexed by the server that it is transmitted to.
# i.e, every relay will have a hash table of the form:
#  Network: 0 -> 1 -> 2 -> 3
#  2's Hash Table: <(3's ip address), T2>
# 2 stores the hash when it is generated, and retrieves when it needs to verify it.

import cPickle as pickle

def storeInHashTable(ip, hash_value):
  try:
    hashes = pickle.load( open( "hashes_forwarded.pickle", "rb" ) )
  except IOError:
    hashes = {}
  hashes[ip] = hash_value
  pickle.dump( hashes, open( "hashes_forwarded.pickle", "wb" ) )

def retrieveFromTable(ip):
  hashes = pickle.load( open( "hashes_forwarded.pickle", "rb" ))
  if ip in hashes:
    hash_value = hashes[ip]
    del hashes[ip]
    pickle.dump( hashes, open( "hashes_forwarded.pickle", "wb" ) )
    return hash_value
  else:
    return "Not Found"