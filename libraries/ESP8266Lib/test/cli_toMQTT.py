#!/usr/bin/env python 
# -*- coding: UTF-8 -*-
# Copyright (c) 2014,OpenThings Projects.
# 接收WiFi设备的数据，然后转发到MQTT的Channel中。

import sys
import os
import time
import serial 
from time import *
from socket import * 

#MQTT Initialize.=======================
try:
    import paho.mqtt.publish as publish
except ImportError:
    # If you have the module installed, just use "import paho.mqtt.publish"
    import os
    import inspect
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
    import paho.mqtt.publish as publish

#======================================
HOST = '192.168.199.191'
#HOST = '192.168.1.7'
PORT = 8888
BUFSIZ = 1024 
ADDR = (HOST, PORT) 

#========================================
strChannel = "/inode/info"
print "Pulish to channel:", strChannel     

#Using Mosquitto MQTT Borker.
#Local Server.
#strBroker = "localhost"
strBroker = "192.168.12.25"
#strBroker = "112.124.67.178"

#==========
tcpCliSock = socket(AF_INET, SOCK_STREAM) 
#tcpCliSock.setdefaulttimeout(20)
tcpCliSock.connect(ADDR) 

print "Receiving..."
while True: 	
	try:
		data = tcpCliSock.recv(BUFSIZ) 
		if (data == "EXIT"): 
		    break 
		
		publish.single(strChannel, data, hostname = strBroker)
    
		data = ctime() + ": " + data
		print "Rev:",data.strip()
		#tcpCliSock.send("Hi: "+data);
		tcpCliSock.send("Data Received.");
	except all as ex:
		print "Error:" + ex
		tcpCliSock.connect(ADDR) 
		print "Reconnected."
		
tcpCliSock.close()
print "TCP Client Closed."

