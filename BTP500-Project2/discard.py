
    if game_state == "multiplayer":
        if game.player1_move and game.player2_move:
            # After both players have chosen their move, display the result
            result = f"Player 1: {game.player1_move} vs Player 2: {game.player2_move}\n"
            result += "Draw!" if game.result == "draw" else f"{game.result} wins!"
            print(result)
            
            # Show the result to both players (or on one screen if you want to display it on both devices)
            return result  # Or, use your existing method to display the result

        # If it's player 1's turn, allow them to pick a move
        if not game.player1_move:
            print("Player 1's turn.")
            game.player1_move = input("Enter your move (rock, paper, scissors): ")
            game.client.send_move(game.player1_move)
        
        # If it's player 2's turn, allow them to pick a move
        if not game.player2_move:
            print("Player 2's turn.")
            game.player2_move = input("Enter your move (rock, paper, scissors): ")
            game.client.send_move(game.player2_move)

        # Wait for the server to process the moves and send back the result
        result = game.client.recv(1024).decode()
        print(result)

    #return None

def draw_menu():
    if draw_button(screen, x=WIDTH//2 - 150, y=HEIGHT//2 - 50, width=300, height=50, text="Local Multiplayer", font=font_medium):
        game_state = "multiplayer"
        start_local_multiplayer()

# That sounds like a fun project! Here are some features you could add to make it more interesting:

# 1. **Multiplayer Mode** – Allow two players to compete instead of just playing against the computer.
# 2. **Best of Three/Five** – Implement a scoring system where players need to win multiple rounds.
# 3. **Timed Rounds** – Add a time limit for each move to increase the challenge.
# 4. **Customizable Themes** – Let players choose different themes (e.g., futuristic, medieval, cartoon).
# 5. **Power-Ups** – Introduce special moves that can be used once per match, like "Double Win" or "Block Move."
# 6. **Leaderboards** – Keep track of high scores and player stats.
# 7. **AI Difficulty Levels** – Have easy, medium, and hard AI opponents.
# 8. **Animated Visuals** – Add fun animations when moves are played.
# 9. **Alternative Hand Signs** – Expand beyond rock-paper-scissors by adding more options like “Lizard-Spock” (from "The Big Bang Theory").
# 10. **Story Mode** – Create a small campaign where the player competes against different characters with increasing difficulty.

# Would you like help implementing any of these ideas?