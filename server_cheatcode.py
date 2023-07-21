
import socket
from threading import Thread

def client_main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        SERVER_HOST = socket.gethostbyname(socket.gethostname())
        SERVER_PORT = 5001 # greater than 5000
        #try to connect
        try:
            s.connect((SERVER_HOST,SERVER_PORT))
            print(f"Connected to {SERVER_HOST}:{SERVER_PORT}")
        
        except Exception as e:
            print('Connection refused')


        def print_recv():
            while True:
                #wait for data
                data = s.recv(1024)
                #disconnected
                if not data: break 
                #recived data
                data = data.decode()
    
            print('Disconnected')
            
        def send(msg):
            #send a msg, must be a string
            s.send(msg.encode()) 
        
        #run print_recv in a thread
        t = Thread(target=print_recv, daemon=True); t.start()
        #wait until disconnected
        t.join() 
        

        '''
        continue here
        '''

    
  










from threading import Thread
import socket



def listen_for_messages(conn,addr):
    while True:
        try:
            data = conn.recv(1024)
        except ConnectionResetError:
            #addr disconnected from server
            break
        if not data:
            #addr disconnected from server
            break
        
        #recived data
        data = data.decode()
        
def listen_for_connections(s):
    while True:
        #wait for a new connection and create a listener for each addr in a different thread
        conn,addr = s.accept()
        t = Thread(target=listen_for_messages,args=(conn,addr),daemon=True)
        t.start()
 
def server_main():  
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        SERVER_HOST = socket.gethostbyname(socket.gethostname())

        SERVER_PORT = 5001

        try:
            s.bind((SERVER_HOST,SERVER_PORT))
            print(f'Binded to: {SERVER_PORT}')
            
        except socket.error as e:
            print(f'Error while connecting to {SERVER_PORT}: {e}')

        #listen for upcoming connections. 
        s.listen()
        print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
        thr = Thread(target=listen_for_connections,args=(s,),daemon=True)
        thr.start()
        
        '''
        Continue here
        '''








