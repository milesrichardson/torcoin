import sys
import hashlib

argc = len(sys.argv)
# print "Argc: " + str(argc)
if (argc < 3 ):
  print "Usage: TCVerify Position Received Hash1 Received Key 1 ..."
  exit(-1)

position = sys.argv[1]
# print "Position: " + position

for i in xrange(argc-1, 2, -2):
  m = hashlib.md5()
  m.update( sys.argv[i] + sys.argv[i - 1])
  # print "    "
  # print i
  # print sys.argv[i]
  # print sys.argv[i -1]
  # print "HexD: " + m.hexdigest()
  if m.hexdigest() != sys.argv[i - 2]:
    print "0"
    exit(-1)
print "1"