from threading import Thread
import socket
import os
import sys

#store the clients addrs
client_connections = []

#separator
SEP = "<SEP>"


def listen_for_messages(conn,addr):
    while True:
        try:
            data = conn.recv(1024)
        except ConnectionResetError:
            #addr disconnected from server
            client_connections.remove(conn)
            print(f'[-]: Disconnected from {addr[0]}:{addr[1]}')
            for c in client_connections:
                if c != conn: 
                    #dont send to itself
                    c.send(f'{addr[0]}{SEP}{addr[1]}{SEP}Se ha desconectado!'.encode())  
            break
        if not data:
            #addr disconnected from server
            client_connections.remove(conn)
            print(f'[-]: Disconnected from {addr[0]}:{addr[1]}')
            for c in client_connections:
                if c != conn: 
                    #dont send to itself
                    c.send(f'{addr[0]}{SEP}{addr[1]}{SEP}Se ha desconectado!'.encode())  
            break
        
        #recived data
        #data = data.decode()
        
        for c in client_connections:
            if c != conn: 
                #dont send to itself
                c.send(f'{addr[0]}{SEP}{addr[1]}{SEP}{data.decode()}'.encode())       
            
        
def listen_for_connections(s):
    while True:
        #wait for a new connection and create a listener for each addr in a different thread
        conn,addr = s.accept()
        client_connections.append(conn)
        print(f'[+]: Connected from {addr[0]}:{addr[1]}')
        
        for c in client_connections:
            if c != conn: 
                #dont send to itself
                c.send(f'{addr[0]}{SEP}{addr[1]}{SEP}Se ha conectado!'.encode())  
    
        t = Thread(target=listen_for_messages,args=(conn,addr),daemon=True)
        t.start()
 
def main():  
    os.system('clear' if sys.platform != 'win32' else 'cls')
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        SERVER_HOST = socket.gethostbyname(socket.gethostname())
        SERVER_PORT = 5001

        try:
            s.bind((SERVER_HOST,SERVER_PORT))
            print(f'[+]: Binded to: {SERVER_PORT}')
            
        except socket.error as e:
            print(f'[!]: Error while connecting to {SERVER_PORT}: {e}')

        #listen for upcoming connections. 
        s.listen()
        print(f"[>]: Listening as {SERVER_HOST}:{SERVER_PORT}")
        listen_for_connections(s)
        

if __name__ == '__main__':
    main()