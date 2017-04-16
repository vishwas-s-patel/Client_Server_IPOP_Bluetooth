import bluetooth
import sys
from bluetooth import *

bt_device_name = "IPOP_BT_DEVICE"
bt_service_name = "IPOP_Bluetooth_Service"

class bluetooth_devices_class():
    def __init__(self):
        self.bt_device_dict = {}
        
    def scan_for_devices(self):
        print "Scanning for BT devices ..."
        nearby_devices = bluetooth.discover_devices()
        for bdaddr in nearby_devices:
            nearby_dev_name = bluetooth.lookup_name(bdaddr)
            if(nearby_dev_name != None):
                if(nearby_dev_name[0:14] == bt_device_name):
                    self.bt_device_dict[nearby_dev_name] = bdaddr

    def read_data(self, device_id):
        if device_id in self.bt_device_dict:
            host = self.bt_device_dict[device_id]
            port = 01
            sock=BluetoothSocket( RFCOMM )
            sock.connect((host, port))
            sock.send("hello!!")
            
            data = sock.recv(1024)
            print "Received data:"
            print data
            print "\n"
            sock.close()

    def list_devices(self):
        print "-----------------------------" 
        print "Available Devices for Service"
        print "-----------------------------" 
        
        for key, value in self.bt_device_dict.items():
            print key + " : " + value
        
        print "========================================"

    def get_devices_list(self):
        return self.bt_device_dict
    
