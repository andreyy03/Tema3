import sys
import socket
import select
import time

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 1024 
PORT = 6666

def chat_server():

    #Create server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))

    #acc max 5 pers, if more they must wait in the lobby
    server_socket.listen(5)
 
    #add clients in socket list
    SOCKET_LIST.append(server_socket)
 
    currentTime = time.ctime(time.time()) + "\r\n"
    print "chat client-server started at port  " + str(PORT) + "\nDate and hour: " + currentTime 
 
    while 1:

        # Select the available list
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
        
        for sock in ready_to_read:
            
            #accept a new connection
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr + "\nDate and hour: " + currentTime
                 
                broadcast(server_socket, sockfd, "[%s:%s] just logged in" % addr)
             
            else:
                
                #server can see client infos
                try:
                    
                    #receive socket`s data, less than 1024kb
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        
                        #there are infos in socket
                        broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)  
                    else:
                        
                        #remove the socket which is out of use   
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        #if there are no more data, the connection is interupted. Send a message to other clients  
                        broadcast(server_socket, sock, "Client (%s, %s) disconnected" % addr) 

                except:
                    broadcast(server_socket, sock, "Client (%s, %s) disconnected" % addr)
                    continue

    server_socket.close()
    
#See the messages sent to all clients connected
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        
      
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                
                socket.close()
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":

    sys.exit(chat_server())         