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
#Script created 8/28/18
#Last modified 9/04/18
#
#This script fingerprints a remote device. It returns
#information about the device's os and configs.
#
#This script must be ran with sudo-
#$>sudo python run.remote.os.and.cli.cmds.py
#
#
#Script tested successfully against the following devices-
#
#



#SSH creds.
#Uncomment the ip address matching your device or add a new one.
#remoteip = "192.168.1.8"
remoteip = "192.168.1.1"
remoteuser = "root"
remotepassword = "sdfsdfsd"
remotetimeout = 0





#Print blank lines.
def printtwolines():
    print (" ")
    print (" ")





#Print blank lines.
def printthreelines():
    print (" ")
    print (" ")
    print (" ")





#Check IP address.
def check_ipaddr(remoteip):
    s=socket(AF_INET,SOCK_STREAM)
    s.settimeout(5)     #5 secomds.
    try:
        s.connect((remoteip,22))
        print (" ")
        print "Successful SSH connection to %s" % (remoteip)
        print (" ")
        s.shutdown(2)
        return True
    except Exception as excmsg:
        print (" ")
        print ("Failed SSH connection to %s") % (remoteip)
        print "Reason - %s" % excmsg
        print (" ")
        return False
        



#Check SSH connection.
check_ipaddr_result = check_ipaddr(remoteip)
#print check_ipaddr_result

if check_ipaddr_result == False:
    exit()
else:
    pass





#Uncomment next line for debugging. Results will print near beginning output.
#print check_ipaddr





def printdashedline():
    dashedline = "-----------"
    print dashedline




#Commas are mandatory. Otherwise each cmd will be parsed and sent one character at a time, instead of as one string.
#Commands to execute on remote device, add support for ifconfig, df, cli/edit mode, etc
#remoteoscommands = ('pwd', 'date', 'uname', 'who',)            #All commas is mandatory, otherwise each string will be parsed and sent character by character.
#Remote OS commands.
remoteoscommands = ('pwd',
        'date',
        'uname -a',
        'w',
        'id',
        'ls',
        'netstat -nat | grep -i listen | grep 128.0.0.1',)     






#http://rtodto.net/running-batch-commands-on-remote-junos-devices
#read this author's py/paramiko code.
#Remote CLI commands.
remoteclicommands = ('cli -c "show version brief"',
        'cli -c "show system uptime"',
        'cli -c "show chassis hardware"',
        'cli -c "show interfaces terse"',
        'cli -c "show pfe version brief"',
        'cli -c "show pfe route ip"',)






totcommands = len(remoteoscommands)
printtwolines()
print ("Command count")
print totcommands




printdashedline()
printtwolines()




def commandlistos():
    header = "These OS commands will be executed on the remote device."
    #print "{0:{1}^10}".format(header, "-")
    #print '{}'.format(remoteoscommands) 
    print (" ")
    print "{0:{1}^10}".format(header, "-")
    print (" ")
    #print '{}'.format(remoteoscommands)
    for r in remoteoscommands:
        print '{}'.format(r)



commandlistos()

printdashedline()
printtwolines()







def commandlistcli():
    header = "These CLI commands will be executed on the remote device."
    print (" ")
    print "{0:{1}^10}".format(header, "-")
    print (" ")
    #print '{}'.format(remoteclicommands)
    for r in remoteclicommands:
        print '{}'.format(r)



commandlistcli()





#Setup SSH connection.
class ssh:
    client = None

    def __init__(self, address, username, password, timeout):

        #Create a new SSH client.
        self.client = client.SSHClient()

        #The following line is required if you want the script to access servers that are not in the known_hosts file.
        self.client.set_missing_host_key_policy(client.AutoAddPolicy())

        #Make the connection.
        #self.client.connect("192.168.1.1", username="root", password="sdfsdfd", look_for_keys="False", timeout=10)
        self.client.connect(remoteip, username=remoteuser, password=remotepassword, look_for_keys="False", timeout=10)


    #def sendCommand(self, command):
    def sendCommand(self, x,command= ()):
        for y in x:
            printthreelines()
            print ("Command executed-->"), y
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
                        #print y
                        #Print as string with utf8 encoding
                        #print(str(self.alldata))
                        print(str.strip(self.alldata))


            else:
                print("Connection not opened.")
            






###Begin OS commands


#Make SSH connection.
def connect(command):
    connection = ssh(remoteip, remoteuser, remotepassword, remotetimeout)
    connection.sendCommand(remoteoscommands)




#Run remote os commands.
print "Command results"
loops = 0
for command in remoteoscommands:
    if loops < 1:
        #print command
        connect(command)
        loops = 1


printdashedline()




###Begin CLI commands


#Make SSH connection.
def connect(command):
    connection = ssh(remoteip, remoteuser, remotepassword, remotetimeout)
    connection.sendCommand(remoteclicommands)




#Run remote cli commands.
loops = 0
for command in remoteclicommands:
    if loops < 1:
        #print command
        connect(command)
        loops = 1





###End of OS commands



#Begin other CLI commands


printtwolines()



exit()




