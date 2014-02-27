#!/usr/bin/env python

import sys
import os
import subprocess
import socket
from optparse import OptionParser
from socket import *

## Let's clear the screen to remove clutter!

subprocess.call('clear',shell=True)

## We need to get the ip address of the host we are scanning

def hosttoip(host):
    try:
        hostip=gethostbyname(host)
        return hostip
    except:
        return None
#
# Need to set up the scan procedure.
#

def scanhost(host, port):
    try:
        scan=socket(AF_INET, SOCK_STREAM)
        scan.connect((host, port))
        return scan
    except:
        scan.close()
        return None
#
# Maybe we can get a banner for the verbose mode if the port is open
#

def getbanner(sock):
    try:
        banner=sock.recv(1024)
        return banner
    except:
        return None
#
# how to handle the scan and what to do
#

def scan(host, port):
    sock=scanhost(host, port)
    setdefaulttimeout(10) 
    if sock:
        if options.verbose=="y" or options.verbose=="yes" or options.verbose=="YES" or options.verbose=="Y":
         print("scanning port:%d"%(port))
         service=os.system("echo 'The known service: '`grep %d /etc/services|head -1|awk {'print $1'}`' (usually)'"%(port)) 
         print("\n")
        banner=getbanner(sock)
        if banner:
	   if options.condition=="OPEN" or options.condition=="open" or options.condition=="ALL" or options.condition=="all" or options.condition==None:
             print("%d     Open\n" %(port))
             if options.verbose=="y" or options.verbose=="yes" or options.verbose=="YES" or options.verbose=="Y":
              print("Banner returned:\n")
	      print("%s"%banner)
        else:
	   if options.condition=="CLOSED" or options.condition=="closed" or options.condition=="ALL" or options.condition=="all" or options.condition==None:
             print("%d     Closed \n" %(port))
        sock.close()
    else:
	 if options.condition=="TIMEOUT" or options.condition=="timeout" or options.condition=="ALL" or options.condition=="all" or options.condition==None:
          print("%d     Timeout\n"%(port))
        
    print "*"*60

if __name__=="__main__":
#
# defining what to do with the options do and some info about them.
#
    parser=OptionParser()
    parser.add_option("-H", "--HOST", dest="host", type="string",
                      help="** you will need to enter a host name or ip**", metavar="example.com")
    parser.add_option("-p", "--port", dest="ports", type="string",
                      help="ports you want to scan separated by comma", metavar="PORT")
    parser.add_option("-f", "--filter",dest="condition",type="string",
		      help="output only the specific condition at the port -->  open, closed, timeout or all", metavar="CONDITION")
    parser.add_option("-v","--verbose",dest="verbose",type="string",
		      help="verbose mode -- yes", metavar="VERBOSE")

    (options, args)=parser.parse_args()
    
    if options.host==None or options.ports==None:
       parser.print_help()
    else:
#
# need to break apart the comma'd ports into a list
#
       host=options.host
       ports=(options.ports).split(",")
       try:  
           ports=list(filter(int, ports))
 
           hostip=hosttoip(host) 
           if hostip:
                print("Now running a scan on %s"%host)
                print("The ip on the host is: %s \n"%hostip)
		print "*"*60
                for port in ports:
                    scan(host, int(port))
           else:
                print("Invalid host (hostname) given\n")
       except:
            print("You have supplied an invalid port list (e.g: -p 21,22,53,..)")
