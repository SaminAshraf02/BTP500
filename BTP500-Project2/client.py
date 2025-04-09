import socket

# Client class to handle communication with the server
class GameClient:
    def __init__(self, host='localhost', port=12345):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def send_move(self, move):
        self.client.send(move.encode())
        result = self.client.recv(1024).decode()
        print(result)
        
    def close(self):
        self.client.close()

# Start client
client = GameClient(host="10.0.0.131", port=12345)  # Replace with the server's local IP

# Example: Player selects 'rock'
client.send_move("rock")
client.close()
