import socket
import threading
import time
import json
import random
import hashlib
import os

threshold = 0.5

def Main():
    host = '127.0.0.1'      # address of server is this machine itself
    port = 5000           # port 1 to 1024 used for core protocols

    s = socket.socket()
    s.bind((host,port))     # binding host and port number of client to the socket of server

    s.listen(5)             # setting up waiting for a TCP connection
    c,addr = s.accept()     # accepting TCP client connection
    c_ack,addr_ack = s.accept()
    print "Connection From: " + str(addr)
    print
    expect_seq_num = 1

    cwd = os.getcwd()
    path = cwd + '/' + "copy"
    f = open(path ,'wb+')     # creates a new file if not there

    while(1):
        checksum_received = c.recv(1024)      # receive checksum
        c.send('F')                           # send the message that hash has been received

        msg = c.recv(1024)  # receive message
        if not msg:
            break
        msg = json.loads(msg)
        c.send('F')
        if msg[1] >= threshold:
            print "Received Packet with Sequence Number:",msg[0]
        seq_num = msg[0]
        prob = msg[1]
        checksum_gen = hashlib.md5(msg[2]).hexdigest()

        if (seq_num == expect_seq_num) and (prob >= threshold) and (checksum_gen == checksum_received):
            ack_msg = ['ACK',seq_num]
            ack_msg = json.dumps(ack_msg, separators=(',',':'))
            print "Sending ACK for Sequence Number:",seq_num
            f.write(msg[2]);
            c_ack.send(ack_msg)
            c_ack.recv(1)
            expect_seq_num = expect_seq_num+1
    c.close()
    c_ack.close()

if __name__ == '__main__':
    Main()
