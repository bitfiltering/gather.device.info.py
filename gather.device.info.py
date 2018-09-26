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
from datetime import datetime
import os



#
#Script created 9/06/18
#Last modified 9/21/18
#
#This script fingerprints a remote device. It returns
#information about the device's os and juniper configs.
#
#This script is ran using sudo-
#$> sudo python gather.device.info.py
#
#
#Script tested successfully against the following devices-
#



#----------------------------------

#SSH creds.
#Uncomment the ip address matching your device or add a new one.
#Change user id and pwd as needed.

##sdfsdf
#remoteip = "1.1.1.1"
#remoteuser = "user"
#remotepassword = "something"

##acd
remoteip = "1.1.1.2"
remoteuser = "root"
remotepassword = "something"

##abc
remoteip = "1.1.1.3"
remoteuser = "root"
remotepassword = "something"



#----------------------------------
remotetimeout = 0







###Setup logging.

#Create output file.
outfile = open('command_output_'+datetime.now().strftime("%d%h%Y")+'.txt',"a+")


#Add a timestamp
def create_output_file():
    #outfile = open('command_output_'+datetime.now().strftime("%d%h%Y")+'.txt',"a+")
    outfile.write('\n')
    outfile.write("This log entry was created on "+datetime.now().strftime("%d%h%Y")+" at "+datetime.now().strftime("%H:%M:%S"))
    outfile.write('\n')
    #return


create_output_file()





#Write to output file.
def write_to_output_file(cmd_results):
#def write_to_output_file():
    #outfile.write("Hello World")
    outfile.write(cmd_results)
    outfile.write('\n')


###End logging setup.







###Check SSH target

#Verify user provided an OS value.
try:
    #Target OS-Juniper, Ubuntu, FreeBSD, etc.
    user_provided_os = sys.argv[1]
except IndexError:
    print " "
    print "Target IP address is " + remoteip
    print "A user can change it by editing the variable "'"remoteip"'" on line 33."
    print " "
    print """Usage:
sudo python gather.device.info.py {--os} {Operating system}

examples:
sudo python gather.device.info.py --os juniper
sudo python gather.device.info.py --os ubuntu
sudo python gather.device.info.py --os cisco
sudo python gather.device.info.py --os freebsd

If you'd like this script to detect the remote 
operating system {os} for you use the 'autodetect' argument.
Example:
sudo python gather.device.info.py --os autodetect

    """

    sys.exit()




#Print blank lines.
def printthreelines():
    print (" ")
    print (" ")
    print (" ")





#Check IP address.
def check_ipaddr(remoteip):
    s=socket(AF_INET,SOCK_STREAM)
    s.settimeout(5)     #Five secomds
    try:
        s.connect((remoteip,22))
        print (" ")
        print "Successful SSH connection to %s" % (remoteip)
        #command_output_saved ("Successful SSH connection to %s" % (remoteip))
        s.shutdown(2)
        return True
    except Exception as excmsg:
        print (" ")
        print ("Failed SSH connection to %s") % (remoteip)
        print "Reason - %s" % excmsg
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









#Juniper OS commands.
remoteoscommands = ('pwd',
        'date',
        'uname -a',
        'w',
        'id',
        'ls',
        'netstat -nat | grep -i listen | grep 128.0.0.1',)


#Juniper CLI commands.
remoteclicommands = ('cli -c "show version brief"',
        'cli -c "show system uptime"',
        'cli -c "show chassis hardware"',
        'cli -c "show interfaces terse"',
        'cli -c "show pfe version brief"',
        'cli -c "show pfe route ip"',)



def junos_commands_tot():
    totcommands = len(remoteoscommands) + len(remoteclicommands)
    print ("Command count")
    print totcommands






#Ubuntu commands ran on remote device.
remoteubuntucommands = ('uptime',
    'uname -a',
    'cat "/etc/issue"',
    'pwd',
    'whoami',)



def ubuntu_commands_tot():
    totcommands = len(remoteubuntucommands)
    print ("Command count")
    print totcommands







def commandlistos():
    header = "These OS commands will be executed on the remote device."
    print (" ")
    print "{0:{1}^10}".format(header, "-")
    print (" ")
    for r in remoteoscommands:
        print '{}'.format(r)



printthreelines()




def commandlistcli():
    header = "These Juniper CLI commands will be executed on the remote device."
    print (" ")
    print "{0:{1}^10}".format(header, "-")
    print (" ")
    for r in remoteclicommands:
        print '{}'.format(r)





def commandlistubuntu():
    header = "These Ubuntu commands will be executed on the remote device."
    print (" ")
    print "{0:{1}^10}".format(header, "-")
    print (" ")
    for r in remoteubuntucommands:
        print '{}'.format(r)





#Setup SSH connection.
class ssh:
    client = None

    def __init__(self, address, username, password, timeout):

        #Create a new SSH client.
        self.client = client.SSHClient()

        #The following line is required if you want the script to access servers that are not in the known_hosts file.
        self.client.set_missing_host_key_policy(client.AutoAddPolicy())

        #Make the connection.
        #self.client.connect("192.168.1.1", username="root", password="Passw0rd!", look_for_keys="False", timeout=10)
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
                        print(str.strip(self.alldata))
                        write_to_output_file(str.strip(self.alldata))


            else:
                print("Connection not opened.")
            
#End of ssh class



if user_provided_os in ['Juniper', 'juniper', 'JUNIPER']:
    junos_commands_tot()
    commandlistos()
    commandlistcli()
    connection = ssh(remoteip, remoteuser, remotepassword, remotetimeout)
    connection.sendCommand(remoteoscommands)
    connection = ssh(remoteip, remoteuser, remotepassword, remotetimeout)
    connection.sendCommand(remoteclicommands)
    sys.exit()



elif user_provided_os in ['ubuntu', 'Ubuntu', 'UBUNTU']:
    ubuntu_commands_tot()
    commandlistubuntu()
    connection = ssh(remoteip, remoteuser, remotepassword, remotetimeout)
    connection.sendCommand(remoteubuntucommands)
    sys.exit()




elif user_provided_os in ['cisco', 'Cisco', 'CISCO']:
    print ("Cisco was selected.")
    printthreelines()
    sys.exit()



elif user_provided_os in ['FreeBSD', 'freebsd', 'freeBSD', 'FREEBSD', 'BSD']:
    print ("FreeBSD was selected.")
    printthreelines()
    sys.exit()



elif user_provided_os in ['autodetect', 'Autodetect', 'AUTODETECT', 'auto']:
    print ("User has requested 'Autodetect'")
    printthreelines()
    sys.exit()



else:
    sys.exit()



printthreelines()

outfile.close()

exit()

