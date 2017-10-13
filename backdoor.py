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

            data = data.decode("utf-8")

            # Remove leading and trailing spaces
            data = data.strip()
            print(data)

            if data == "help":
                self.request.sendall(
                    bytearray("The supported commands are pwd, cd, cwd, ls, cp, rm, mv, cat, snap, diff", "utf-8"))

            elif data == "ls":
                # Run a subprocess in shell that returns output of ls -l into variable
                output = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                # Decode the shell command result into a string format
                lsCommand = output.stdout.decode("utf-8")

                # Send the string output to the client
                self.request.sendall(bytearray(lsCommand, "utf-8"))

            elif data == "pwd":

                # Run a subprocess in shell that returns output of pwd into variable
                output = subprocess.run(['pwd'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                # Decode the shell command result into a string format
                pwdCommand = output.stdout.decode("utf-8")

                # Send the string output to the client
                self.request.sendall(bytearray(pwdCommand, "utf-8"))

                # If cat command is given without any parameters, display usage error
            elif data == "cat":
                self.request.sendall(bytearray("USAGE: cat 'file-name'\n", "utf-8"))

            elif data[0:4] == "cat ":

                # Strip any spaces in-between cat and command
                command = str.strip(data[4:])

                try:

                    print("INSIDE COMMAND: " + command)
                    # Run a subprocess in shell that returns output of cat into variable
                    output = subprocess.run(['cat', command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                    # Decode the shell command result into a string format
                    catCommand = output.stdout.decode("utf-8")

                    # Send the string output to the client
                    self.request.sendall(bytearray(catCommand, "utf-8"))

                except:

                    print("FileNotFoundError")


            elif data == "who":

                # Run a subprocess in shell that returns output of who into variable
                output = subprocess.run(['who'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                # Decode the shell command result into a string format
                whoCommand = output.stdout.decode("utf-8")

                # Send the string output to the client
                self.request.sendall(bytearray(whoCommand, "utf-8"))

            elif data == "net":

                # Run a subprocess in shell that returns output of net into variable
                output = subprocess.run(['net'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                # Decode the shell command result into a string format
                netCommand = output.stdout.decode("utf-8")

                # Send the string output to the client
                self.request.sendall(bytearray(netCommand, "utf-8"))

            elif data == "ps":

                # Run a subprocess in shell that returns output of ps into variable
                output = subprocess.run(['ps'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                # Decode the shell command result into a string format
                psCommand = output.stdout.decode("utf-8")

                # Send the string output to the client
                self.request.sendall(bytearray(psCommand, "utf-8"))

            elif data == "uptime":

                # Run a subprocess in shell that returns output of uptime into variable
                output = subprocess.run(['uptime'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                # Decode the shell command result into a string format
                uptimeCommand = output.stdout.decode("utf-8")

                # Send the string output to the client
                self.request.sendall(bytearray(uptimeCommand, "utf-8"))



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
