#########################################################################
#
# MQTTPort
#
# Copyright (c) 2017 Eckhart Koeppen
# 
# panStamp  is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
# 
# panStamp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with panStamp; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 
# USA
#
#########################################################################

from swap.SwapException import SwapException
from urlparse import urlparse

import threading
import serial
import time, sys
import Queue
import datetime

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(userdata.rx_topic)


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    userdata.serial_received(msg.payload)


class MQTTPort(threading.Thread):
    """
    Wrapper class of the pyserial package
    """

    def run(self):
        """
        Run serial port listener on its own thread
        """
        self._go_on = True
        while self._go_on:
            self.client.loop()
            if not self._strtosend.empty():
                strpacket = self._strtosend.get()          
                self.client.publish(self.tx_topic, strpacket) 
        print "Closing MQTT connection..."

    
    def stop(self):
        """
        Stop serial port
        """
        self._go_on = False

    def send(self, buf):
        """
        Send string buffer via serial
        
        @param buf: Packet to be transmitted
        """
        self._strtosend.put(buf)


    def setRxCallback(self, cb_function):
        """
        Set callback reception function. This function is called whenever a new serial packet
        is received from the gateway
        
        @param cb_function: User-defined callback function
        """
        self.serial_received = cb_function


    def reset(self):
        """
        Hardware reset serial modem
        """
        pass

           
    def __init__(self, server="mqtt://localhost:1883/serial", verbose=False):
        """
        Class constructor
        
        @param portname: Name/path of the serial port
        @param speed: Serial baudrate in bps
        @param verbose: Print out SWAP traffic (True or False)
        """
        threading.Thread.__init__(self)
        self.portname = server
        self.serial_received = None
        self._strtosend = Queue.Queue()
        self._verbose = verbose
        self.client = mqtt.Client("lagarto", True, self)
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        p = urlparse(server)
        self.topic = p.path[1:]

        self.client.connect(p.hostname, p.port, 60)

