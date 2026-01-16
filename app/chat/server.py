import threading
import socket

host = '10.0.240.220'
port = 10001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = list()
nicknames = list()

def broadcast(message):
    for client in clients:
        client.send(message.encode('ascii'))

def handle(client):
    #this function is going to handle the messages coming from the client and broadcasting it to every client present in that server at that time and if someone left the server then this function also handles to remove that client from the server too 
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            broadcast(message)
            if not message:
                raise Exception("Client disconnected")
                
        except:
            # if the client left the server then this whole thing will work to remove that client
            if client in clients: 
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f"{nickname} has left the chat!!")
                nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat')
        client.send("connected to the server".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening")
receive()




