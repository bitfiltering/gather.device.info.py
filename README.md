import paramiko

from paramiko import client
paramiko.util.log_to_file('/tmp/paramiko.log')
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import threading
from threading import Thread
import sys
import time
from socket import *



#
#Script created 8/8/18
#Last modified 8/22/18
#
#This script fingerprints a remote device. It returns
#information about the device's hardware, software, etc.
#
#
#This script must be ran with sudo-
#$>sudo python gather.device.info.py
#
#
#Script tested successfully against the following devices-
#
#



#SSH creds.
remoteip = "192.168.1.1"
remoteuser = "root"
remotepassword = "something"
remotetimeout = 0




#Print blank lines.
def printtwolines():
    print (" ")
    print (" ")




#Get user input for commands to run remotely. This step should be interactive.
#All commas are mandatory, otherwise each cmd will be parsed and sent one character at a time, instead of as one string.
#Commands to execute on remote device, add support for ifconfig, df, cli/edit mode, etc
#remotecommands = ('uname -a', 'ls', 'pwd', 'date',)
#remotecommands = ('pwd', 'date', 'uname', 'who',)            #All commas is mandatory, otherwise each string will be parsed and sent character by character.
remotecommands = ('pwd',
        'date',
        'uname',
        'w',)     





totcommands = len(remotecommands)
printtwolines()
print ("Total number of commands to execute->"), totcommands





def commandlist():
    print(" ")
    print ("Commands being executed-")
    print '{}'.format(remotecommands) 



#commandlist()
printtwolines()




#Setup SSH connection.
class ssh:
    client = None

    def __init__(self, address, username, password, timeout):

        #Create a new SSH client.
        self.client = client.SSHClient()

        #The following line is required if you want the script to access servers that are not in the known_hosts file.
        self.client.set_missing_host_key_policy(client.AutoAddPolicy())

        #Make the connection.
        #self.client.connect("192.168.1.1", username="root", password="something", look_for_keys="False", timeout=10)
        self.client.connect(remoteip, username=remoteuser, password=remotepassword, look_for_keys="False", timeout=10)


    #def sendCommand(self, command):
    def sendCommand(self, x,command= ()):
        for y in x:
            #Check if connection is made previously
            if(self.client):
                #stdin, stdout, stderr = self.client.exec_command(command)
                stdin, stdout, stderr = self.client.exec_command(y)
                while not stdout.channel.exit_status_ready():
                    #Print stdout data when available
                    if stdout.channel.recv_ready():
                        #Retrieve the first 1024 bytes
                        self.alldata = stdout.channel.recv(1024)
                        while stdout.channel.recv_ready():
                            #Retrieve the next 1024 bytes
                            self.alldata += stdout.channel.recv(1024)


                        #Print command and results.
                        print y
                        #Print as string with utf8 encoding
                        print(str(self.alldata))



            else:
                print("Connection not opened.")
            



#Make SSH connection.
def connect(command):
    connection = ssh(remoteip, remoteuser, remotepassword, remotetimeout)
    connection.sendCommand(remotecommands)






loops = 0
for command in remotecommands:
    if loops < 1:
        #print command
        connect(command)
        loops = 1







#Next line prints results of last command.
#print (str(connection.alldata))



#results = (connection.alldata)
#print results()
#connection.sendCommand(alldata)



printtwolines()




#Print device hw, sw, etc.
#print ("** ")
#print '{}'.format(commandresults) 
#print (" ")




#self.results = []
    #self.results.append(self.alldata)
    #for r in self.results:
    #print(r) + (" ")
    #print (" ")
    #print r





#Add other network devices here



exit()



