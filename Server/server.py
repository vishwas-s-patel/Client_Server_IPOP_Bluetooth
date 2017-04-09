import socket                   # Import socket module
import logging
import json

import socket
from threading import Thread
from SocketServer import ThreadingMixIn

IPOP_IP = '172.31.0.1'
IPOP_PORT = 5222
BUFFER_SIZE = 1024

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print " New thread started for "+ip+":"+str(port)

    def run(self):
        filename='mytext.txt'
        f = open(filename,'rb')
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                self.sock.send(l)
                #print('Sent ',repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                self.sock.close()
                break


class ClientPort():
    def __init__(self,ip,port,sock):
        self.ip = ip
        self.port = port
        self.sock = sock
        print "New Client REQ received "+ip+":"+str(port)

    def get_open_port(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("",0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return port

    def set_new_port(self, port):
        self.port = port

    def send_new_port_to_client(self, port):
        self.sock.send(str(port))        
        data = self.sock.recv()
        print "================="
        print data
        print "================="

        if(data == 'ACK'):
            return 0
        else:
            return 1

if __name__ == '__main__':
    ipop_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ipop_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ipop_sock.bind((IPOP_IP, IPOP_PORT))
    threads = []
    
    while True:        
        ipop_sock.listen(5)
        
        print "Waiting for incoming connections..."
        (conn, (ip,port)) = ipop_sock.accept()

        print 'Got connection from ', (ip,port)
        ##################################################################################
        # Create the client Port and tell the client to recieve data from different port #
        ##################################################################################
        '''newClient = ClientPort(ip, port, conn)
        new_port = newClient.get_open_port()
        print "new_port " + str(new_port)

        if(newClient.send_new_port_to_client(new_port)):
            print "Client ACK the new port: " + new_port
        else:
            print "Client NOT_ACK the new port: " + new_port

        newClient.set_port(new_port)'''
        ####################################################
        # Create new threads for every new Client request  #
        ####################################################
        newthread = ClientThread(ip, port, conn)
        newthread.start()
        threads.append(newthread)
        
    for t in threads:
        t.join()

