import socketserver
import socket, threading
import hashlib
dad23 

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
           self.request.sendall( bytearray( "You said: " + data, "utf-8"))
           print("%s (%s) wrote: %s" % (self.client_address[0], 
                 threading.currentThread().getName(), data.strip()))

if __name__ == "__main__":
   HOST, PORT = "localhost", 9999
   server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
   server.serve_forever()

f = open( "test.txt", "rb")
sha = hashlib.sha256()
while True:
    data = f.read(4096)
    if not data:
        break
    sha.update(data)
f.close()

print(sha.hexdigest())
