import socketserver
import socket, threading
import hashlib
import sys
import subprocess
import os

class MyTCPHandler(socketserver.BaseRequestHandler):
    BUFFER_SIZE = 4096
    closeServer = False

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

            # If cd command is given without any parameters, display usage error
            elif data == "cd":
                self.request.sendall(bytearray("USAGE: cd 'directory'\n", "utf-8"))

            elif data[0:3] == "cd ":

                # Strip any spaces in-between cd and command
                command = str.strip(data[3:])

                try:

                    # Change the current directory based on the provided argument
                    os.chdir(command)

                    # Indicate successful cd to client
                    self.request.sendall(bytearray("Success!\n", "utf-8"))

                except:

                    self.request.sendall(bytearray("cd: " + command + ": No such file or directory\n", "utf-8"))
                    # If cat command is given without any parameters, display usage error

            elif data == "rm":
                self.request.sendall(bytearray("USAGE: rm 'file-name'\n", "utf-8"))

            elif data[0:3] == "rm ":

                # Strip any spaces in-between cat and command
                command = str.strip(data[3:])

                try:

                    # Run a subprocess in shell that returns output of rm into variable
                    output = subprocess.run(['rm', command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                    # Decode the shell command result into a string format
                    rmCommand = output.stdout.decode("utf-8")

                    # Send the string output to the client
                    self.request.sendall(bytearray(rmCommand, "utf-8"))

                except:

                    self.request.sendall(bytearray("rm: " + command + ": No such file or directory\n", "utf-8"))

            elif data[0:3] == "cp ":

                # Strip any spaces in-between cat and command
                command = str.strip(data[3:])

                try:

                    # Run a subprocess in shell that returns output of rm into variable
                    output = subprocess.run(['rm', command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                    # Decode the shell command result into a string format
                    rmCommand = output.stdout.decode("utf-8")

                    # Send the string output to the client
                    self.request.sendall(bytearray(rmCommand, "utf-8"))

                except:

                    self.request.sendall(bytearray("rm: " + command + ": No such file or directory\n", "utf-8"))


            elif data == "logout":

                #Disconnect the client from the server
                self.request.sendall(bytearray("You have logged out of the server\n", "utf-8"))

                #Break out of the while loop for the client thread, disconnecting the client
                break

            elif data == "off":
                #Set close server flag
                self.closeServer = True
                # Break out of while loop, shutting off server
                break


        if self.closeServer == True:

            #Tell the serve_forever() loop to stop (shut down server)
            server.shutdown()

            #Clean up the server
            server.server_close()




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
