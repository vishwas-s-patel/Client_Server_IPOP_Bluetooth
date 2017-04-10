import socket

TCP_IP = '172.31.0.1'
TCP_PORT = 5222
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((TCP_IP, TCP_PORT))


with open('received_file', 'wb') as f:
    print 'file opened'
    while True:
        data = s.recv(BUFFER_SIZE)
        data1 = s1.recv(BUFFER_SIZE)
        print('data=%s', (data))
        print('data1=%s', (data))
        if not data:
            f.close()
            print 'file close()'
            break
        # write data to a file
        f.write(data)
        f.write(data1)

print('Successfully get the file')
s.close()
s1.close()
print('connection closed')
