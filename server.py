#server
import socket
import threading

#define constants:
HEADER = 8
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

client2_data = " "

#create server socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    global client2_data
    print("[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        #because the first message sent is blank
        #if we try to get the lengh it will crash
        #so we skip it till we get a value
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")
    

            #send message to client
            conn.send("Message Received".encode(FORMAT))

    conn.close()

def start_server():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        #wait for new connetion from client
        conn, addr = server.accept()
        #create a new thread to handle the new connection
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNETIONS] {threading.activeCount() - 1}")

print("[STARTING SERVER]")
start_server()

