import socket                   # Import socket module
import logging
import json
from bt_nodes import bluetooth_devices_class

import socket
from threading import Thread
from SocketServer import ThreadingMixIn

IPOP_IP = '172.31.0.1'
IPOP_PORT = 5222
BUFFER_SIZE = 1024

class ServerThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        
        self.bt_devices = bluetooth_devices_class()
        self.bt_devices.scan_for_devices()
        self.bt_devices.list_devices()
        
        print "New thread started for "+ip+":"+str(port)

    def run(self):
        self.sock.send('220 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nWelcome to IPOP Network of Bluetooth Nodes!\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        
        while True:
            cmd = self.sock.recv(BUFFER_SIZE)
            if not cmd: 
                break
            else:
                print 'Received: ', cmd
                try:
                    func = getattr(self, cmd[:4].strip().upper())
                    func(cmd)
                except Exception, e:
                    print 'Error:', e
                    self.sock.send('Sorry! Encountered error.\r\n')
                    
    
    def LIST(self, cmd):
        device_list = self.bt_devices.get_devices_list()
       
        bt = '' 
        for key in device_list.keys():
            bt += key + '\n'
       
        packet_len = str(len(bt))
        
        head_len_list = list("00000")
        packet_len_list = list(packet_len)
        
        it = -1
        
        for i in range(len(packet_len_list)):
            head_len_list[it] = packet_len_list[it]
            it = it -1 
        
        packed_packet_len = ''.join(head_len_list)

        header = '150 ' + packed_packet_len + ' '
        
        self.sock.send(header)

        self.sock.send(bt)

    def READ(self, cmd):
        if(len(cmd) <= 5):
            self.sock.send("Try again with appropriate command")
        else:
            device_id = cmd[5:22]
            data = self.bt_devices.read_data(device_id)
            self.sock.send(data)
       
    def SCAN(self, cmd):
        self.bt_devices.scan_for_devices()
        self.sock.send("300 OK")  
     
if __name__ == '__main__':
    ipop_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ipop_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ipop_sock.bind((IPOP_IP, IPOP_PORT))
    threads = []
   
    device_id = "IPOP_BT_DEVICE_01"
    
    while True:        
        ipop_sock.listen(5)
        
        print "Waiting for incoming connections..."
        
        (conn, (ip,port)) = ipop_sock.accept()

        print 'Got connection from ', (ip,port)
        ####################################################
        # Create new threads for every new Client request  #
        ####################################################
        
        newthread = ServerThread(ip, port, conn)
        newthread.daemon = True
        newthread.start()
        
        threads.append(newthread)
        
    for t in threads:
        t.join()
