import socket

def Client(player1_pos, player2_pos):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5555))

    while True:
        client_socket.send(f"{player1_pos[0]},{player1_pos[1]}".encode())
        data = client_socket.recv(1024).decode()
        if not data:
            break
        player2_pos[0], player2_pos[1] = map(int, data.split(','))

    client_socket.close()
