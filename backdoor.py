import socketserver
import socket, threading
import hashlib
import sys
import subprocess

class MyTCPHandler(socketserver.BaseRequestHandler):
   BUFFER_SIZE = 4096

   def handle(self):

       while 1:
           data = self.request.recv(self.BUFFER_SIZE)

           if len(data) == self.BUFFER_SIZE:
               while 1:

                   try:  # error means no more data
                       data += self.request.recv(self.BUFFER_SIZE, socket.MSG_DONTWAIT)

                   except:
                       break

           if len(data) == 0:
               break

           data = data.decode( "utf-8")

           #Remove leading and trailing spaces
           data = data.strip()
           print(data)
           if data == "help":
               self.request.sendall( bytearray("The supported commands are pwd, cd, cwd, ls, cp, rm, mv, cat, snap, diff", "utf-8"))

           if data == "ls":

           print("%s (%s) wrote: %s" % (self.client_address[0],
                 threading.currentThread().getName(), data.strip()))

if __name__ == "__main__":
   HOST = "localhost"
   PORT = int(sys.argv[1])
   server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
   server.serve_forever()

'''
f = open( "test.txt", "rb")
sha = hashlib.sha256()
while True:
    data = f.read(4096)
    if not data:
        break
    sha.update(data)
f.close()

print(sha.hexdigest())
'''
