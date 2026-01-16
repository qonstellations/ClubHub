import socket
import threading

host ='10.0.240.220'
port = 10001

nickname = input("Choose a nickname")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))

            else:
                print(message)

        except:
            print("An error occured")
            client.close()
            break
def write():
    while True:
        try:
            message = f'{nickname}: {input("")}'
            client.send(message.encode('ascii'))

        except (EOFError, KeyboardInterrupt):
            # This happens if you press Ctrl+C or the stream ends
            print("\nDisconnecting...")
            client.close()
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
