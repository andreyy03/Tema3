"""
Le premier prgramme en Python
* utilisation des arguments de la lignne de commande
* les processus
* le logger
@author Dragos STOICA
@version 0.6
@date 17.feb.2014
"""

import sys
import socket
import select
 
def chat_client():
    if(len(sys.argv) < 3) :
        print "Invalid command. You must add for connection:  python chat_client.py hostname port"
        sys.exit()

    host = sys.argv[1] #Read first command argv (hostname)
    port = int(sys.argv[2]) #Read second command argv (port number)

    #counter for number of connected clients
    #clients_counter = 0
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    #Connection to host
    try :
        s.connect((host, port))
        ##clients_counter = 1
    except :
        print 'Connexion impossible'
        sys.exit()
     
    #if there are no more clients, one person can`t talk
    #if(clients_counter < 2):
    #    print "Not enough members yet. Wait for others" 
    #elif(clients_counter > 2):
    #    print 'connection etablished. you can write now'
    #    sys.stdout.write('[Moi] '); sys.stdout.flush()
    
    print 'connection etablished. you can write now'
    sys.stdout.write('[Moi] '); sys.stdout.flush()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        #List of sockets available
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])

        for sock in ready_to_read:             
            if sock == s:
                #server data
                data = sock.recv(1024)
                    
                if not data :
                    print '\nDisconnected'
                    sys.exit()
                else :
                    #Show message
                    sys.stdout.write(data)
                    sys.stdout.write('[Moi] '); sys.stdout.flush()     
                
            else :
                #The current user sent a message
                msg = sys.stdin.readline()
                s.send(msg)
                sys.stdout.write('[Moi] '); sys.stdout.flush() 
        
if __name__ == "__main__":

    sys.exit(chat_client())