import socket
import threading
import time
import json
import random
import hashlib
import os
from termcolor import colored

sent_flag = []          # if timeout make sent_flag in window = 0;
ACK_num = []
packet_list = []

def get_prob():
    return random.randint(1,10)/10.0
    # return 1

def divide_file(file,n):        # going to divide the file into n packets, each packet except last has size(file)/n size and last packet has different size
    cwd = os.getcwd()
    path = cwd + '/' + file
    f = open(path,'r+')
    size_file = os.path.getsize(path)
    print size_file
    packet_size = (size_file)/n
    for i in range(1,n):
        content = f.read(packet_size)
        packet_list.append(content)
    content = f.read(size_file - ((n-1)*(packet_size)))
    packet_list.append(content)
    print packet_list

def send_packet(seq_num,s):
    data = packet_list[seq_num-1]
    # data = "I Am Packet Number " + str(seq_num)
    checksum = hashlib.md5(data).hexdigest()      # for sending the hash
    s.send(checksum)
    s.recv(1)     # receieve the message that hash has been sent
    print_string = "Sending Packet with Sequence Number " + str(seq_num)
    print print_string
    prob = get_prob()
    msg = [seq_num,prob,data]
    msg = json.dumps(msg, separators=(',',':'))
    sent_flag[seq_num] = 1
    s.send(msg)



def get_ACK(a,s):
    while(1):
        msg = s.recv(1024)
        s.send('F')
        if not msg:
            break
        msg1 = msg
        msg = json.loads(msg)
        if msg[0] == 'ACK':
            ACK_num[msg[1]] = 1
            # print_string = "ACK Received for Packet with Sequence Number: " + str(msg[1])
            # print print_string
            print msg1

def Main():
    host = '127.0.0.1'              # address of client that wants to connect
    port = 5000

    s = socket.socket()
    s.connect((host,port))          # connecting client to the socket

    s_ack = socket.socket()
    s_ack.connect((host,port))          # connecting client to the socket

    file1 = raw_input("Enter File Name: ")
    w = int(raw_input("Enter Window Size: "))
    timeout = float(raw_input("Enter Timeout Time: "))
    n = int(raw_input("Enter Number of Packets: "))
    print
    if w<=0:
        raise ValueError('Window Size should be greater than 0')
    if n<0:
        raise ValueError('Number of Packets should be Non-Negative')
    for i in range(1,n+2):
        sent_flag.append(0)
        ACK_num.append(0)

    t1 = threading.Thread( target=get_ACK, args=(1,s_ack) )
    t1.start()

    win_base = 1
    divide_file(file1,n)
    timee = time.time()             # present time
    while win_base+w-1 < n:
        for j in range(win_base,win_base+w):
            if sent_flag[j] == 0:
                send_packet(j,s)
                s.recv(1)
        presenttime = time.time()
        if presenttime - timee > timeout:
            print "\nTimeout Occurred : Resending and Resetting Timer"
            for j in range(win_base,win_base+w):
                sent_flag[j] = 0
            timee = time.time()
            continue
        elif ACK_num[win_base] == 1:
            win_base = win_base+1
            timee = time.time()

        # if not timeout and ACK received of seq num = win_base:
        #     win_base = win_base + 1
        # elif timeout:
        #     sent_flag[whole window] = 0


    pointer = n-w+1         # for the leftover last w packets , for which the window cannot traverse any further
    if n < w:
        pointer = 1         # if no. of packets < window size then this condition takes place because client has to send packets from 1 to n
    timee = time.time()
    while pointer <= n:
        for j in range(pointer,n+1):
            if sent_flag[j] == 0:
                send_packet(j,s)
                s.recv(1)
        presenttime = time.time()
        if presenttime - timee > timeout:
            print "\nTimeout Occurred : Resending and Resetting Timer"
            for j in range(pointer,n+1):
                sent_flag[j] = 0
            timee = time.time()
            continue
        elif ACK_num[pointer] == 1:
            pointer = pointer+1
            timee = time.time()

    s.close()

    print
    print colored('Completed Transfer of Packets','green')
    print


if __name__ == '__main__':
    Main()
