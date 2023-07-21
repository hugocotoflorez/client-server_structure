import socket
from threading import Thread
import sys
import os

#separator
SEP = "<SEP>"

contacts = {}

def main():
    os.system('clear' if sys.platform != 'win32' else 'cls')
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        SERVER_HOST = x if (x:=input("[>]: SERVER HOST: ")).lower()!= 'auto' else socket.gethostbyname(socket.gethostname())
        SERVER_PORT = 5001 # greater than 5000
        #try to connect
        try:
            s.connect((SERVER_HOST,SERVER_PORT))
            print(f"[+]: Connected to {SERVER_HOST}:{SERVER_PORT}")

        
        except Exception as e:
            print('[!]: Connection refused')

        else:
            def print_recv():
                while True:
                    #wait for data
                    try:
                        data = s.recv(1024)
                    #disconnected
                    except Exception:break
                    #disconnected
                    if not data: break 
                    #recived data
                    ip_addr, local_addr,data = data.decode().split(SEP)
                    
                    print(f'[>]: ({contacts.get(local_addr,local_addr)}) {data}')
        
                print('Disconnected')
                
            def send(msg):
                #send a msg, must be a string
                s.send(msg.encode()) 
            
            #run print_recv in a thread
            t = Thread(target=print_recv, daemon=True); t.start()
            
            while True:
                try:
                    msg = input()
                    if msg == 'q': break
                    
                    elif msg.startswith('/add'):
                        _, addr, name = msg.split(' ')
                        contacts.update({addr:name})
                        
                    else:
                        send(msg)
                
                except KeyboardInterrupt:
                    print('[>]: Disconnecting...',end=' ')
                    sys.exit()

                    
        
        
if __name__ == '__main__':
    main()