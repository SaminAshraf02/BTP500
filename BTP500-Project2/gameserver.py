import socket
import threading

# Server class to handle connections
class GameServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)  # Waiting for 2 players (client connections)
        self.connections = []
        self.moves = {}
        self.game_running = False

    def start(self):
        print("Server started. Waiting for players...")
        while len(self.connections) < 2:
            client, addr = self.server.accept()
            print(f"Player connected from {addr}")
            self.connections.append(client)
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        while True:
            move = client.recv(1024).decode()
            if move:
                # Store player move
                self.moves[client] = move
                # Check if both players have made their move
                if len(self.moves) == 2:
                    self.check_winner()
                    self.reset_game()
                    
    def check_winner(self):
        player1_move = self.moves[self.connections[0]]
        player2_move = self.moves[self.connections[1]]
        
        result = self.get_game_result(player1_move, player2_move)
        for conn in self.connections:
            conn.send(f"Player 1 move: {player1_move}, Player 2 move: {player2_move}. Result: {result}".encode())

    def get_game_result(self, player1_move, player2_move):
        if player1_move == player2_move:
            return "Draw"
        elif (player1_move == "rock" and player2_move == "scissors") or \
             (player1_move == "paper" and player2_move == "rock") or \
             (player1_move == "scissors" and player2_move == "paper"):
            return "Player 1 wins"
        else:
            return "Player 2 wins"
    
    def reset_game(self):
        self.moves.clear()

    def close(self):
        for conn in self.connections:
            conn.close()
        self.server.close()

# Start server
server = GameServer()
server.start()