from socket import *
import threading
import random

# connection
server_port = 12000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(5)
print('The server is ready to receive')

def simple_math(connection_socket : socket):
    """
    connection_socket.send(f"Write 'exit' to end connection\n".encode())
    connection_socket.send(f"Write 'random' to get a random number between two integers of your input.\n - The smaller number MUST be written first.\n".encode())
    connection_socket.send(f"Write 'add' to get the sum of two integers of your input.\n".encode())
    connection_socket.send(f"Write 'subtract' to get the difference between two integers of your input.\n - The second number will be subtracted from the first.\n".encode())
    connection_socket.send(f"\n".encode())
    """
    
    while True:
        connection_socket.send(f'Please enter a command.\n'.encode())
        message = connection_socket.recv(1024).decode().strip()
        
        if message == 'stop' or message == 'quit' or message == 'exit':
            connection_socket.send(f'Terminating service.\n'.encode())
            connection_socket.close()
            break
        print(f'Received message: {message}\n'.encode())
        
        # connection_socket.send(f'Please input two numbers separated by a space.\n'.encode())
        
        # getting another message accepted by the server
        numbers = connection_socket.recv(1024).decode().strip()
        
        nmb = numbers.strip().split(' ')
        number_one = int(nmb[0])
        number_two = int(nmb[1])
        
        if message == 'random':
            result = random.randint(number_one, number_two)
        if message == 'add':
            result = number_one + number_two
        if message == 'subtract':
            result = number_one - number_two
            
        connection_socket.send(f'{result}\n'.encode())

# three-way handshake
while True:
    connection_socket, addr = server_socket.accept()
    print(f'Connection established with {addr}')
    threading.Thread(target=simple_math, args=(connection_socket,)).start()