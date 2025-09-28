from socket import *
import threading
import json
import random

# connection
server_port = 12000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(1)
print('The server is ready to receive')

def simple_math(connection_socket : socket):
    connection_socket.send(f"Write 'exit' to end connection\n".encode())
    connection_socket.send(f"Write 'random' to get a random number between two integers of your input.\n - The smaller number MUST be written first.\n".encode())
    connection_socket.send(f"Write 'add' to get the sum of two integers of your input.\n".encode())
    connection_socket.send(f"Write 'subtract' to get the difference between two integers of your input.\n - The second number will be subtracted from the first.\n".encode())
    connection_socket.send(f"\n".encode())
    
    while True:
        connection_socket.send(f"Please enter a command written as a json string.\n".encode())
        connection_socket.send('The format should be: {"method": "<command>", "number_one": <int>, "number_two": <int>}\n'.encode())
        message = json.loads(connection_socket.recv(1024).decode().strip())
        
        if message["method"] == 'stop' or message["method"] == 'quit' or message["method"] == 'exit':
            connection_socket.send(f'Terminating service.\n'.encode())
            break
        print(f'Received message: {message}\n'.encode())
        
        number_one = message["number_one"]
        number_two = message["number_two"]
        
        if message["method"] == 'random':
            result = random.randint(number_one, number_two)
        
        if message["method"] == 'add':
            result = number_one + number_two
        
        if message["method"] == 'subtract':
            result = number_one - number_two
            
        connection_socket.send(f"{result}\n".encode())

# three-way handshake
while True:
    connection_socket, addr = server_socket.accept()
    print(f'Connection established with {addr}')
    # longer_dialogue(connection_socket)
    # threading is for concurrent connections
    threading.Thread(target=simple_math, args=(connection_socket,)).start()
