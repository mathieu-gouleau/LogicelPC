# file: rfcomm-client.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a client application that uses RFCOMM sockets
#       intended for use with rfcomm-server
#
# $Id: rfcomm-client.py 424 2006-08-24 03:35:54Z albert $

from bluetooth import *
import sys

addr = "dc:a6:32:49:ff:0e"

if len(sys.argv) < 2:
    print "no device specified.  Searching all nearby bluetooth devices for"
    print "the SampleServer service"
else:
    addr = sys.argv[1]
    print "Searching for SampleServer on %s" % addr

# search for the SampleServer service
uuid = "ef2ea8b-042f-47f5-953e-577d8060de55"
service_matches = find_service( uuid = uuid, address = addr )

if len(service_matches) == 0:
    print "couldn't find the SampleServer service =("
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]
print(port)

print "connecting to \"%s\" on %s" % (name, host)

# Create the client socket
sock=BluetoothSocket( RFCOMM )
sock.connect((host, port))

print "connected.  type stuff"
while True:
    data = raw_input()
    if len(data) == 0: break
    sock.send(data)

sock.close()