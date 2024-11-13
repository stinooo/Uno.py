import socket

def Server(player1_pos, player2_pos):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5555))
    server_socket.listen(1)
    print("Server started, waiting for a connection...")
    conn, addr = server_socket.accept()
    print(f"Connection from {addr} has been established!")

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        player2_pos[0], player2_pos[1] = map(int, data.split(','))
        conn.send(f"{player1_pos[0]},{player1_pos[1]}".encode())

    conn.close()
