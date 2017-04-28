# Go_Back_N_Protocol
This is the simulation of Basic Go-Back-N protocol where the sender sends N consecutive packets, which form the window, in a single stretch without waiting for the ACK to be received for the packet and the window moves forward when an ACK is received by the First member of the window.
If this doesn't happen within a specified time or there is packet loss for any member of the window, the whole window's packets are retransmitted.
To generate packet loss, probability of acceptance for each packet was generated and each packet was lost at the receiver's end randomly.
Also the packets here are those of a file broken into K packets, where K is an input given by the user. The file is copied into another file named "copy" present in the same directory 
