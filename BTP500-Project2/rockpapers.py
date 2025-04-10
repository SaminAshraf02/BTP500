#####################################################################################################
#####################################################################################################
###                                                                                               ###
###     BTP_500 PROJECT BTP500 Project 2: Building a Game in Python Using Data Structures         ###
###                                                                                               ###
###                     Project Submission Deadline: April 12th                                   ###
###                                                                                               ###
###                                GROUP MEMBERS                                                  ### 
###                                                                                               ###
###          1.JUNHO LEE                                      xxxxx                               ###
###          2.MICHAEL MELLES                                111838223                            ###
###          3.SAMIN ASHRAF                                  140362229                            ###
###                                                                                               ###
#####################################################################################################
#####################################################################################################

# Imports necessary for the project
import pygame
import random
import sys
from collections import deque
import time
from pygame import mixer
import os

# Initialize pygame
pygame.init()
mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Rock-Paper-Scissors")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (238, 123, 144)
GREEN = (0, 205, 0)
BLUE = (0, 0, 255)
YELLOW = (215, 165, 0)
PURPLE = (157, 123, 238)
ORANGE = (247, 190, 172)
PERIWINKLE = (123, 163, 238)
MINT = (123, 238, 204)
LAVENDER = (194, 172, 247)
CYAN = (172, 247, 246)

# Fonts
font_large = pygame.font.SysFont('Arial', 50, bold=True)
font_medium = pygame.font.SysFont('Arial', 30, bold=True)
font_small = pygame.font.SysFont('Arial', 20)
font_title = pygame.font.SysFont('Arial', 60, bold=True)

# Game states
MENU = 0
PLAYING = 1
RESULT = 2
TOURNAMENT = 3
DOUBLE_CHOICE = 4
KOREAN_RPS = 5
CONGRATULATIONS = 6
TIMED_GAME = 7
game_state = MENU


# Load images
def load_image(name, scale=1):

    # Load images with proper error handling and naming
    image_files = {
        'rock': '/Users/saminashraf/Documents/GitHub/BTP500/BTP500-Project2/rock.png',
        'paper': '/Users/saminashraf/Documents/GitHub/BTP500/BTP500-Project2/paper.png',
        'scissors': '/Users/saminashraf/Documents/GitHub/BTP500/BTP500-Project2/scissor.png'
    }
    
    # Error handling in case the images are not present or do not load
    try:
        img = pygame.image.load(image_files[name]).convert_alpha()
        if scale != 1:
            img = pygame.transform.smoothscale(img, 
                (int(img.get_width() * scale), 
                 int(img.get_height() * scale)))
        return img
    except Exception as e:
        print(f"Error loading {image_files[name]}: {e}")
        # Create detailed fallback graphics
        surf = pygame.Surface((100, 100), pygame.SRCALPHA)
        if name == 'rock':
            pygame.draw.circle(surf, (0, 0, 255), (50, 50), 45)
            pygame.draw.circle(surf, (0, 0, 200), (50, 50), 40)
        elif name == 'paper':
            pygame.draw.rect(surf, (255, 255, 255), (10, 10, 80, 80))
            pygame.draw.line(surf, (200, 200, 200), (20, 20), (80, 80), 5)
        elif name == 'scissors':
            points = [(35, 15), (85, 85), (15, 85)]
            pygame.draw.polygon(surf, (255, 0, 0), points)
            pygame.draw.polygon(surf, (200, 0, 0), [(40, 20), (80, 80), (20, 80)])
        return pygame.transform.smoothscale(surf, (int(100*scale), int(100*scale)))

# Load images with corrected names
rock_img = load_image('rock', 0.5)
paper_img = load_image('paper', 0.5)
scissors_img = load_image('scissors', 0.5)

# Load background images
menu_bg = pygame.Surface((WIDTH, HEIGHT))
menu_bg.fill((20, 20, 40))
game_bg = pygame.Surface((WIDTH, HEIGHT))
game_bg.fill((30, 30, 50))

# Load button images
button_normal = pygame.Surface((300, 60))
button_normal.fill((70, 70, 100))
button_hover = pygame.Surface((300, 60))
button_hover.fill((100, 100, 130))
button_click = pygame.Surface((300, 60))
button_click.fill((50, 50, 80))

# Load sounds
try:
    win_sound = mixer.Sound('win.wav')
    lose_sound = mixer.Sound('lose.wav')
    draw_sound = mixer.Sound('draw.wav')
    click_sound = mixer.Sound('click.wav')
except:
    # Fallback if sounds aren't available
    win_sound = None
    lose_sound = None
    draw_sound = None
    click_sound = None

class Tournament:
    def __init__(self):
        self.players = deque()
        self.current_match = None
        self.winners = deque()
        self.first_round_done = False
        
    def add_player(self, name):
        self.players.append(name)
        
    def next_match(self):
        # FIRST ROUND: Avoid human vs human if not done yet
        if not self.first_round_done:
            humans = [p for p in self.players if not p.is_ai]
            ais = [p for p in self.players if p.is_ai]
            temp_players = deque()

            # Pair each human with an AI if possible
            while humans and ais:
                temp_players.append(humans.pop())
                temp_players.append(ais.pop())

            # Any leftover players (all AI or leftover humans)
            leftovers = humans + ais
            for player in leftovers:
                temp_players.append(player)

            self.players = temp_players
            self.first_round_done = True

        if len(self.players) >= 2:
            self.current_match = (self.players.popleft(), self.players.popleft())
            return self.current_match
        return None
    
    def declare_winner(self, winner):
        if winner:
            self.winners.append(winner)

        if len(self.players) <= 1:
            # Move winners to players for next round
            if len(self.players) == 1:
                self.winners.append(self.players.popleft())

            if len(self.winners) > 1:
                self.players = self.winners
                self.winners = deque()
            elif len(self.winners) == 1:
                return True  # Final winner
        return False
    
class Player:
    def __init__(self, name, is_ai=False, ai_level=1):
        self.name = name
        self.is_ai = is_ai
        self.ai_level = ai_level
        self.score = 0
        self.move_history = deque(maxlen=10)  # Track last 10 moves for AI
        
    def make_move(self, opponent_history=None):
        if not self.is_ai:
            return None  # Human player makes move through UI
        
        if self.ai_level == 1:
            # Level 1: Random choices
            return random.choice(['rock', 'paper', 'scissors'])
        elif self.ai_level == 2:
            # Level 2: Simple pattern recognition
            if len(opponent_history) > 2:
                # If opponent repeats moves, counter the most common one
                last_move = opponent_history[-1]
                if opponent_history.count(last_move) > 2:
                    return self.get_counter(last_move)
            return random.choice(['rock', 'paper', 'scissors'])
        elif self.ai_level == 3:
            if len(opponent_history) > 3:
                # Convert deque to indexed form using enumerate
                pattern = tuple(opponent_history)[-3:]  # This part is safe since tuple() allows indexing
                hist_tuple = tuple(opponent_history)    # Tuples support indexing and slicing

                possible_next = []
                for i in range(len(hist_tuple) - 3):
                    if tuple(hist_tuple[i:i + 3]) == pattern and i + 3 < len(hist_tuple):
                        possible_next.append(hist_tuple[i + 3])

                if possible_next:
                    predicted = random.choice(possible_next)
                    return self.get_counter(predicted)

            # Fallback to level 2 behavior
            if len(opponent_history) > 0:
                return self.get_counter(random.choice(opponent_history))
            return random.choice(['rock', 'paper', 'scissors'])
            
    def get_counter(self, move):
        if move == 'rock':
            return 'paper'
        elif move == 'paper':
            return 'scissors'
        else:
            return 'rock'
        
    def record_move(self, move):
        self.move_history.append(move)

class Game:
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.player1_move = None
        self.player2_move = None
        self.result = None
        self.animation_frame = 0
        self.max_animation_frames = 30
        self.tournament = None
        self.final_tournament_winner = None
        self.game_history = []
        self.timed_mode = False
        
    def start_single_player(self, player_name, ai_level):
        self.player1 = Player(player_name)
        self.player2 = Player("Computer", is_ai=True, ai_level=ai_level)
        self.tournament = None
        self.reset_round()
        pygame.event.clear()
        pygame.event.wait()

    def start_timed_game(self, player_name, ai_level, time_limit):
        self.player1 = Player(player_name)
        self.player2 = Player("Computer", is_ai=True, ai_level=ai_level)
        self.tournament = None
        self.reset_round()
        global selected_time, countdown_active, countdown_start_time
        # Initialize the timer and difficulty
        selected_time = time_limit  # Selected by the player in the menu
        countdown_active = False
        countdown_start_time = 0
        pygame.event.clear()
        pygame.event.wait()
        
    def start_tournament(self, players):
        self.tournament = Tournament()
        for player in players:
            self.tournament.add_player(player)
        self.next_tournament_match()
        
    def next_tournament_match(self):
        if self.tournament:
            match = self.tournament.next_match()
            if match:
                self.player1, self.player2 = match
                self.reset_round()
                return True
        return False
    
    def reset_round(self):
        self.player1_move = None
        self.player2_move = None
        self.result = None
        self.animation_frame = 0

    def make_move(self, player, move):
        if player == 1:
            self.player1_move = move
            self.player1.record_move(move)
        else:
            self.player2_move = move
            self.player2.record_move(move)
            
        # If both moves are made, determine result
        if self.player1_move and self.player2_move:
            self.determine_result()
            
    def determine_result(self):
        move1 = self.player1_move
        move2 = self.player2_move
        
        if move1 == move2:
            self.result = 'draw'
            if draw_sound:
                draw_sound.play()
        elif (move1 == 'rock' and move2 == 'scissors') or \
             (move1 == 'paper' and move2 == 'rock') or \
             (move1 == 'scissors' and move2 == 'paper'):
            self.result = 'player1'
            self.player1.score += 1
            if win_sound:
                win_sound.play()
        else:
            self.result = 'player2'
            self.player2.score += 1
            if lose_sound:
                lose_sound.play()
        
        # Record game history
        self.game_history.append({
            'player1': self.player1.name,
            'player2': self.player2.name,
            'move1': move1,
            'move2': move2,
            'result': self.result
        })
    
    def update_animation(self):
        if self.animation_frame < self.max_animation_frames:
            self.animation_frame += 1
    
    def is_animating(self):
        return self.animation_frame < self.max_animation_frames
    
    def get_tournament_winner(self):
        if self.tournament and len(self.tournament.winners) == 1:
            return self.tournament.winners[0]
        return None

# Main game instance
game = Game()

def draw_button(screen, x, y, width, height, text, font, **kwargs):
    # Set default colors
    text_color = kwargs.get('text_color', BLACK)
    normal_color = kwargs.get('normal_color', (70, 70, 100))
    hover_color = kwargs.get('hover_color', (100, 100, 130))
    click_color = kwargs.get('click_color', (50, 50, 80))
    border_color = kwargs.get('border_color', (30, 30, 50))
    
    # Validate colors
    def validate_color(color):
        if isinstance(color, str):
            # Handle color names like "GREEN", "RED" etc.
            return globals().get(color, (70, 70, 100))
        elif isinstance(color, (tuple, list)) and len(color) == 3:
            return tuple(max(0, min(255, c)) for c in color)  # Clamp values
        return (70, 70, 100)  # Default fallback
    
    normal_color = validate_color(normal_color)
    hover_color = validate_color(hover_color)
    click_color = validate_color(click_color)
    border_color = validate_color(border_color)
    text_color = validate_color(text_color)
    
    mouse_pos = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()[0]
    
    if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
        if clicked:
            color = click_color
        else:
            color = hover_color
    else:
        color = normal_color
    
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)
    pygame.draw.rect(screen, border_color, (x, y, width, height), 3, border_radius=10)
    
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width//2, y + height//2))
    screen.blit(text_surface, text_rect)
    
    return (x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height and clicked)


def draw_menu():
    screen.blit(menu_bg, (0, 0))
    
    # Title with shadow effect
    title = font_title.render("Rock Paper Scissors", True, (200, 200, 255))
    shadow = font_title.render("Rock Paper Scissors", True, (50, 50, 80))
    screen.blit(shadow, (WIDTH//2 - title.get_width()//2 + 3, 103))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    # Draw buttons
    buttons = [
        ("Classic Challenge", 200, MINT),
        ("Tournament", 280, PERIWINKLE),
        ("Race Against Time", 360, PURPLE),
        # ("Double Choice Mode", 360, PURPLE),
        ("Korean RPS Mode", 440, ORANGE),
        ("Quit", 520, RED)
    ]
    
    for text, y, color in buttons:
        if draw_button(screen, WIDTH//2 - 150, y, 300, 60, text, font_medium, normal_color=color):
            if click_sound:
                click_sound.play()
            if text == "Classic Challenge":
                return "single_player_menu"
            elif text == "Tournament":
                return "tournament_menu"
            elif text == "Double Choice Mode":
                return "double_choice"
            elif text == "Korean RPS Mode":
                return "korean_rps"
            elif text == "Quit":
                return "quit"
            elif text == "Race Against Time":
                return "timer_menu"
    
    # Instructions
    instructions = font_small.render("Select a game mode to begin", True, WHITE)
    screen.blit(instructions, (((WIDTH//2 - instructions.get_width()//2) + 3), 610))
    
    return None

# Global variables necessary for Race Against Time
selected_time = 10 # Default time value
countdown_active = False
countdown_start_time = 0
time_left = 0
game_result = None

def draw_timed_menu():
    global input_active, player_name, selected_time, selected_difficulty

    screen.fill((20, 20, 40))

    # Player's Name Input Label
    title = font_large.render("Race Against Time", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
    
    # Player's Name Input
    name_label = font_medium.render("Name:", True, WHITE)
    screen.blit(name_label, (WIDTH//2 - 150, 185))

    # Name input
    pygame.draw.rect(screen, (50, 50, 70), (WIDTH//2 - 150, 220, 300, 40), border_radius=5)
    pygame.draw.rect(screen, (100, 100, 130) if input_active else (70, 70, 100), 
                    (WIDTH//2 - 150, 220, 300, 40), 2, border_radius=5)
    player_name_input = font_medium.render(player_name if player_name else "Player", True, WHITE)
    screen.blit(player_name_input, (WIDTH//2 - 140, 225))

    # Time limit label
    time_limit_label = font_medium.render("Time Limit: (Default: 10s)", True, WHITE)
    screen.blit(time_limit_label, (WIDTH//2 - 150, 280))

    # 5s button
    if draw_button(screen=screen, 
               x=WIDTH//2 - 150, 
               y=315, 
               width=85, 
               height=50, 
               text="5s", 
               font=font_medium,  
               normal_color=RED):
        if click_sound: click_sound.play()
        selected_time = 5

    # 10s button
    if draw_button(screen=screen, 
               x=WIDTH//2 - 65, 
               y=315, 
               width=85, 
               height=50, 
               text="10s", 
               font=font_medium,  
               normal_color=LAVENDER):
        if click_sound: click_sound.play()
        selected_time = 10

    # 15s button
    if draw_button(screen=screen, 
               x=WIDTH//2 + 20, 
               y=315, 
               width=85, 
               height=50, 
               text="15s", 
               font=font_medium,  
               normal_color=PERIWINKLE):
        if click_sound: click_sound.play()
        selected_time = 15

    # AI Difficulty
    diff_label = font_medium.render("Difficulty", True, WHITE)
    screen.blit(diff_label, (WIDTH//2 - 150, 400))
    
    # Easy button
    if draw_button(screen=screen, 
               x=WIDTH//2 - 150, 
               y=400, 
               width=85, 
               height=50, 
               text="Easy", 
               font=font_medium,  
               normal_color=PERIWINKLE):
        if click_sound: click_sound.play()
        return ("set_difficulty", 1)

    # Medium Button
    if draw_button(screen=screen, 
               x=WIDTH//2 - 65,
               y=400, 
               width=125,
               height=50, 
               text="Medium", 
               font=font_medium,  
               normal_color=PURPLE):
        if click_sound: click_sound.play()
        return ("set_difficulty", 2)

    # Hard Button
    if draw_button(screen=screen, 
               x=WIDTH//2 + 60, 
               y=400, 
               width=90, 
               height=50, 
               text="Hard", 
               font=font_medium,  
               normal_color=RED):
        if click_sound: click_sound.play()
        return ("set_difficulty", 3)

    # Start Game button
    if draw_button(screen=screen,
                  x=WIDTH//2 - 150,
                  y=550,
                  width=300,
                  height=60,
                  text="Start Game",
                  font=font_medium,
                  normal_color=MINT):
        if click_sound: click_sound.play()
        return ("start_timed", player_name if player_name else "Player", selected_difficulty, selected_time)

    # Back button
    if draw_button(screen=screen,
                  x=WIDTH//2 - 150,
                  y=480,
                  width=300,
                  height=60,
                  text="Back",
                  font=font_medium):
        if click_sound: click_sound.play()
        return "menu"
    
    return None

def draw_timed_game():
    # Handle the race against time gameplay
    global countdown_active, countdown_start_time, time_left, game_result
    
    screen.fill((30, 30, 50))
    
    # Player scores display
    p1_score = font_medium.render(f"{game.player1.name}: {game.player1.score}", True, WHITE)
    p2_score = font_medium.render(f"{game.player2.name}: {game.player2.score}", True, WHITE)
    screen.blit(p1_score, (50, 30))
    screen.blit(p2_score, (WIDTH - 50 - p2_score.get_width(), 30))
    
    # Draw the timer
    if countdown_active:
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - countdown_start_time) / 1000  # in seconds
        time_left = max(0, selected_time - elapsed)
        
        # Format timer display
        timer_color = RED if time_left < 2 else PERIWINKLE if time_left < 5 else WHITE
        timer_text = font_large.render(f"{time_left:.1f}", True, timer_color)
        screen.blit(timer_text, (WIDTH//2 - timer_text.get_width()//2, 80))
        
        # Time's up
        if time_left <= 0 and not game.player1_move:
            game_result = "Time's up! You lose."
            countdown_active = False
            game.make_move(1, random.choice(['rock', 'paper', 'scissors']))  # Random move if time's up
            game.make_move(2, game.player2.make_move(game.player1.move_history))
    
    # Game area
    if game.player1_move and game.player2_move and game.is_animating():
        # Animation for moves (same as regular game)
        game.update_animation()
        progress = game.animation_frame / game.max_animation_frames

        # Animate player 1's choice
        if game.player1_move:
            img = rock_img if game.player1_move == 'rock' else paper_img if game.player1_move == 'paper' else scissors_img
            x = 150 * progress
            screen.blit(img, (x, HEIGHT//2 - img.get_height()//2))
        else:
            q = font_large.render("?", True, WHITE)
            screen.blit(q, (150 * progress, HEIGHT//2 - 25))

        # Animate player 2's choice
        if game.player2_move:
            img = rock_img if game.player2_move == 'rock' else paper_img if game.player2_move == 'paper' else scissors_img
            x = WIDTH - 150 * progress - img.get_width()
            screen.blit(img, (x, HEIGHT//2 - img.get_height()//2))
        else:
            q = font_large.render("?", True, WHITE)
            screen.blit(q, (WIDTH - 150 * progress - 50, HEIGHT//2 - 25))

        # VS text during animation
        if 0.3 < progress < 0.7:
            vs = font_large.render("VS", True, RED)
            screen.blit(vs, (WIDTH//2 - vs.get_width()//2, HEIGHT//2 - 25))
    else:
        if game.player1_move and game.player2_move:
            # Show final results
            img1 = rock_img if game.player1_move == 'rock' else paper_img if game.player1_move == 'paper' else scissors_img
            img2 = rock_img if game.player2_move == 'rock' else paper_img if game.player2_move == 'paper' else scissors_img
            
            screen.blit(img1, (150, HEIGHT//2 - img1.get_height()//2))
            screen.blit(img2, (WIDTH - 150 - img2.get_width(), HEIGHT//2 - img2.get_height()//2))
            
            # Result text
            if game_result:
                result_text = font_large.render(game_result, True, RED)
            elif game.result == 'player1':
                result_text = font_large.render(f"{game.player1.name} wins!", True, GREEN)
            elif game.result == 'player2':
                result_text = font_large.render(f"{game.player2.name} wins!", True, GREEN)
            else:
                result_text = font_large.render("Draw!", True, YELLOW)
            screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, HEIGHT//2 - 175))
            
            # Next round button
            if draw_button(screen=screen,
                         x=WIDTH//2 - 150,
                         y=HEIGHT - 100,
                         width=300,
                         height=50,
                         text="Next Round",
                         font=font_medium):
                if click_sound: click_sound.play()
                game.reset_round()
                game_result = None
                # Reset and start timer
                countdown_active = True
                countdown_start_time = pygame.time.get_ticks()
        else:
            # Player selection phase
            if not game.player1_move and not game.player1.is_ai:
                # Only start timer if it's not already active
                if not countdown_active:
                    countdown_active = True
                    countdown_start_time = pygame.time.get_ticks()
                
                select_text = font_medium.render(f"{game.player1.name}, choose quickly!", True, WHITE)
                screen.blit(select_text, (WIDTH//2 - select_text.get_width()//2, 150))
                
                # Calculate positions for images
                spacing = 200
                start_x = (WIDTH//2 - spacing * 1.5) + 40
                images = [
                    (rock_img, start_x, 'rock'),
                    (paper_img, start_x + spacing, 'paper'),
                    (scissors_img, start_x + spacing * 2, 'scissors')
                ]
                
                for img, x, move in images:
                    img_rect = img.get_rect(center=(x + 75, HEIGHT//2 + 50))
                    screen.blit(img, img_rect)
                    
                    # Hover effect
                    mouse_pos = pygame.mouse.get_pos()
                    if img_rect.collidepoint(mouse_pos):
                        pygame.draw.rect(screen, YELLOW, img_rect.inflate(10, 10), 3, border_radius=5)
                        
                        # Handle click
                        if pygame.mouse.get_pressed()[0]:
                            if click_sound: click_sound.play()
                            countdown_active = False  # Stop timer once move is made
                            game.make_move(1, move)
                            # AI makes move immediately after player
                            game.make_move(2, game.player2.make_move(game.player1.move_history))

    # Quit button
    if draw_button(screen=screen,
                  x=WIDTH - 120,
                  y=HEIGHT - 60,
                  width=100,
                  height=40,
                  text="Quit",
                  font=font_small):
        if click_sound: click_sound.play()
        return "menu"
    
    return None

def draw_single_player_menu():
    screen.fill((20, 20, 40))
    
    title = font_large.render("Classic Challenge", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
    
    # Name input label
    name_label = font_medium.render("Name:", True, WHITE)
    screen.blit(name_label, (WIDTH//2 - 150, 185))  # Position it above the input box

    # Name input
    pygame.draw.rect(screen, (50, 50, 70), (WIDTH//2 - 150, 220, 300, 40), border_radius=5)
    pygame.draw.rect(screen, (100, 100, 130) if input_active else (70, 70, 100), 
                    (WIDTH//2 - 150, 220, 300, 40), 2, border_radius=5)
    name_text = font_medium.render(player_name if player_name else "Player", True, WHITE)
    screen.blit(name_text, (WIDTH//2 - 140, 225))
    
    # Difficulty level
    diff_label = font_medium.render("Difficulty:", True, WHITE)
    screen.blit(diff_label, (WIDTH//2 - 150, 285))
    
    # Easy button
    if draw_button(screen=screen, 
               x=WIDTH//2 - 150, 
               y=320, 
               width=85, 
               height=50, 
               text="Easy", 
               font=font_medium,  
               normal_color=PERIWINKLE):
        if click_sound: click_sound.play()
        return ("set_difficulty", 1)

    # Medium Button
    if draw_button(screen=screen, 
               x=WIDTH//2 - 65,
               y=320, 
               width=125,
               height=50, 
               text="Medium", 
               font=font_medium,  
               normal_color=PURPLE):
        if click_sound: click_sound.play()
        return ("set_difficulty", 2)

    # Hard Button
    if draw_button(screen=screen, 
               x=WIDTH//2 + 60, 
               y=320, 
               width=90, 
               height=50, 
               text="Hard", 
               font=font_medium,  
               normal_color=RED):
        if click_sound: click_sound.play()
        return ("set_difficulty", 3)
    
    # Start button
    if draw_button(screen=screen,
                  x=WIDTH//2 - 150,
                  y=420,
                  width=300,
                  height=60,
                  text="Start Game",
                  font=font_medium,
                  normal_color=MINT):
        if click_sound: click_sound.play()
        return ("start_single", player_name if player_name else "Player", selected_difficulty)

    # Back button
    if draw_button(screen=screen,
                  x=WIDTH//2 - 150,
                  y=490,
                  width=300,
                  height=60,
                  text="Back",
                  font=font_medium):
        if click_sound: click_sound.play()
        return "menu"
    
    return None

def draw_tournament_menu():
    screen.blit(menu_bg, (0, 0))
    
    title = font_large.render("Tournament Mode", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
    
    # Player names input
    name_label = font_medium.render("Player names (comma separated):", True, WHITE)
    screen.blit(name_label, (WIDTH//2 - 250, 180))
    
    # Input box
    pygame.draw.rect(screen, (50, 50, 70), (WIDTH//2 - 250, 220, 500, 40), border_radius=5)
    pygame.draw.rect(screen, (100, 100, 130) if tournament_input_active else (70, 70, 100), 
                    (WIDTH//2 - 250, 220, 500, 40), 2, border_radius=5)
    names_text = font_medium.render(tournament_names if tournament_names else "Player1,Player2", True, WHITE)
    screen.blit(names_text, (WIDTH//2 - 240, 225))
    
    # Example text
    example = font_small.render("Example: Player1,Player2,Player3", True, (150, 150, 150))
    screen.blit(example, (WIDTH//2 - example.get_width()//2, 270))
    
    # Back button
    if draw_button(screen, WIDTH//2 - 150, 500, 300, 60, "Back", font_medium):
        if click_sound:
            click_sound.play()
        time.sleep(0.2)
        return "menu"
    
    # Start Tournament button - using keyword arguments for clarity
    if draw_button(screen, 
                  x=WIDTH//2 - 150, 
                  y=425, 
                  width=300, 
                  height=60, 
                  text="Start Tournament", 
                  font=font_medium,
                  text_color=BLACK,
                  normal_color=GREEN,
                  hover_color=(GREEN[0]+30, GREEN[1]+30, GREEN[2]+30),
                  click_color=(GREEN[0]-20, GREEN[1]-20, GREEN[2]-20)):
        if click_sound:
            click_sound.play()
        time.sleep(0.2)
        names = [name.strip() for name in tournament_names.split(",")]
        names = names[:4]
        players = deque()
        for name in names:
            players.append(Player(name))

        players.append(Player("AI_Easy", is_ai=True, ai_level=1))
        players.append(Player("AI_Medium", is_ai=True, ai_level=2))
        players.append(Player("AI_Hard", is_ai=True, ai_level=3))

        if len(players) >= 2:
            return ("start_tournament", players)
        else:
            error_text = font_small.render("Need at least 2 players!", True, RED)
            screen.blit(error_text, (WIDTH//2 - error_text.get_width()//2, 470))
    
    return None

def random_two_choices():
    return random.sample(['rock', 'paper', 'scissors'], 2)

def best_ai_move(ai_choices, player_choices):
    win_condition= {
        'rock': 'scissors',
        'paper': 'rock',
        'scissors': 'paper'
    }

    best_move = ai_choices[0]
    best_score = float('-inf')

    for ai_move in ai_choices:
        score = 0
        for player_move in player_choices:
            if ai_move == player_move:
                score += 0  # Draw
            elif win_condition[ai_move] == player_move:
                score += 1  # Win
            else:
                score -= 1  # Loss
        if score > best_score:
            best_score = score
            best_move = ai_move

    return best_move

def reset_double_choice():
    global double_choice_stage, player_choices, ai_choices, player_final, ai_final, is_win
    double_choice_stage = 0
    player_choices = []
    ai_choices = []
    player_final = None
    ai_final = None
    is_win = False

#double choice game
def draw_double_choice_game():
    global double_choice_stage, player_choices, ai_choices, player_final, ai_final, player_wins_double, computer_wins_double, is_win

    if final_winner and not is_win:
        if final_winner == 1:
            player_wins_double += 1
        elif final_winner == 2:
            computer_wins_double += 1
        is_win = True

    screen.fill((40, 40, 60))
    if double_choice_stage == 0:
        # Difficulty selection
        diff_label = font_medium.render("Select AI Difficulty:", True, WHITE)
        screen.blit(diff_label, (WIDTH//2 - diff_label.get_width()//2, 20))
        score_text = font_small.render(f"Player Wins: {player_wins_double}   Computer Wins: {computer_wins_double}", True, WHITE)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 150))
        difficulties = [
            ("Easy", WIDTH//2 - 160, 100, GREEN, 1),
            ("Medium", WIDTH//2 - 50, 100, YELLOW, 2),
            ("Hard", WIDTH//2 + 60, 100, RED, 3)
        ]

        for text, x, y, color, level in difficulties:
            if draw_button(screen=screen,
                           x=x, y=y,
                           width=80, height=40,
                           text=text,
                           font=font_small,
                           normal_color=color):
                global double_choice_difficulty
                double_choice_difficulty = level
                if click_sound: click_sound.play()
    
    if double_choice_stage == 0:
        prompt = font_medium.render("Choose TWO different moves:", True, WHITE)
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 50))

        spacing = 150
        start_x = WIDTH//2 - spacing * 1.5
        moves = ['rock', 'paper', 'scissors']
        images = [rock_img, paper_img, scissors_img]

        for i, move in enumerate(moves):
            img = images[i]
            x = start_x + i * spacing
            img_rect = img.get_rect(center=(x + 75, HEIGHT//2))
            screen.blit(img, img_rect)

            mouse_pos = pygame.mouse.get_pos()
            if img_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, YELLOW, img_rect.inflate(10, 10), 3)
                if event.type == pygame.MOUSEBUTTONDOWN and img_rect.collidepoint(pygame.mouse.get_pos()):
                    if move not in player_choices:
                        if click_sound: click_sound.play()
                        player_choices.append(move)
                        time.sleep(0.2)

        if len(player_choices) == 2:
            ai_choices = random_two_choices()
            double_choice_stage = 1

    elif double_choice_stage == 1:
        title = font_medium.render("Now pick ONE from your two choices!", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))

        spacing = 250
        start_x = WIDTH//4
        for i, move in enumerate(player_choices):
            img = rock_img if move == 'rock' else paper_img if move == 'paper' else scissors_img
            x = start_x + i * spacing
            img_rect = img.get_rect(center=(x, HEIGHT//2))
            screen.blit(img, img_rect)

            mouse_pos = pygame.mouse.get_pos()
            if img_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, GREEN, img_rect.inflate(10, 10), 3)
                if pygame.mouse.get_pressed()[0]:
                    if click_sound: click_sound.play()
                    player_final = move
                    if double_choice_difficulty == 1:
                        ai_final = random.choice(ai_choices)
                    elif double_choice_difficulty == 2:
                        ai_final = best_ai_move(ai_choices, player_choices) if random.random() > 0.3 else random.choice(ai_choices)
                    else:
                        ai_final = best_ai_move(ai_choices, player_choices)
                    double_choice_stage = 2
                    time.sleep(0.2)

        ai_label = font_small.render("Opponent Choices:", True, WHITE)
        screen.blit(ai_label, (WIDTH//2 - ai_label.get_width()//2, HEIGHT//2 + 100))
        for i, move in enumerate(ai_choices):
            img = rock_img if move == 'rock' else paper_img if move == 'paper' else scissors_img
            x = WIDTH//2 - 100 + i * 120
            screen.blit(img, (x, HEIGHT//2 + 130))

    elif double_choice_stage == 2:
        p_img = rock_img if player_final == 'rock' else paper_img if player_final == 'paper' else scissors_img
        a_img = rock_img if ai_final == 'rock' else paper_img if ai_final == 'paper' else scissors_img

        screen.blit(p_img, (150, HEIGHT//2 - p_img.get_height()//2))
        screen.blit(a_img, (WIDTH - 150 - a_img.get_width(), HEIGHT//2 - a_img.get_height()//2))

        vs_text = font_large.render("VS", True, RED)
        screen.blit(vs_text, (WIDTH//2 - vs_text.get_width()//2, HEIGHT//2 - 40))

        if player_final == ai_final:
            result = "It's a draw!"
        elif (player_final == 'rock' and ai_final == 'scissors') or \
            (player_final == 'paper' and ai_final == 'rock') or \
            (player_final == 'scissors' and ai_final == 'paper'):
            result = "You Win!"
            if not is_win:
                player_wins_double += 1
                is_win = True
        else:
            result = "Opponent Wins!"
            if not is_win:
                computer_wins_double += 1
                is_win = True

        result_text = font_medium.render(result, True, YELLOW)
        screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, 80))

        if draw_button(screen, WIDTH//2 - 150, HEIGHT - 100, 300, 50, "Play Again", font_medium):
            reset_double_choice()
            
            if click_sound: click_sound.play()

        if draw_button(screen, WIDTH - 120, HEIGHT - 60, 100, 40, "Quit", font_small):
            if click_sound: click_sound.play()
            time.sleep(0.2)
            return "menu"
        
    if draw_button(screen,
               x=20,
               y=HEIGHT - 60,
               width=160,
               height=40,
               text="Back to Menu",
               font=font_small):
        if click_sound:
            click_sound.play()
        # Reset state
        reset_double_choice()
        return "menu"

    return None

def reset_korean_rps():
    global stage, attacker, round_winner, final_winner
    global player_move, ai_move, is_win
    global krps_ai, krps_player, krps_player_history, krps_ai_history

    stage = "initial"
    attacker = None
    round_winner = None
    final_winner = None
    player_move = None
    ai_move = None
    is_win = False

    # Clear move histories
    krps_player_history.clear()
    krps_ai_history.clear()

    krps_player = Player("You")
    # Fixed AI level (e.g., level 1)
    krps_ai = Player("AI", is_ai=True, ai_level=3)

def draw_korean_rps():
    #game logic
    global stage, attacker, player_move, ai_move, final_winner
    #win counter
    global player_wins_korean, computer_wins_korean, is_win
    #previous moves
    global krps_ai, krps_player, krps_player_history, krps_ai_history

    # Fill the background
    screen.fill((25, 25, 50))

    # Draw title and score
    title = font_large.render("Korean Rock Paper Scissors", True, WHITE)
    score_text = font_small.render(f"Player Wins: {player_wins_korean}   Computer Wins: {computer_wins_korean}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 75))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))

    # Determine and display attacker's label
    attacker_label = ""
    if attacker == 1:
        attacker_label = "You are guessing!"
    elif attacker == 2:
        attacker_label = "Computer is guessing!"
    elif stage == "initial":
        attacker_label = "Play to determine who guesses first!"
    attacker_text = font_medium.render(attacker_label, True, YELLOW)
    screen.blit(attacker_text, (WIDTH//2 - attacker_text.get_width()//2, 100))

    # If the game round is complete, display the result and current round’s move images.
    if final_winner and not is_win:
        if final_winner == 1:
            player_wins_korean += 1
        elif final_winner == 2:
            computer_wins_korean += 1
        is_win = True

    if final_winner:
        result = f"{'You' if final_winner == 1 else 'Computer'} won the game!"
        result_text = font_large.render(result, True, GREEN)
        screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, 160))

        # Show moves with images for the current round
        player_label = font_medium.render("You played:", True, WHITE)
        screen.blit(player_label, (150, 250))
        ai_label = font_medium.render("Computer played:", True, WHITE)
        screen.blit(ai_label, (WIDTH - 300, 250))
        def get_image(move):
            return rock_img if move == 'rock' else paper_img if move == 'paper' else scissors_img
        if player_move:
            screen.blit(get_image(player_move), (150, 300))
        if ai_move:
            screen.blit(get_image(ai_move), (WIDTH - 300, 300))

        if draw_button(screen, WIDTH//2 - 150, HEIGHT - 120, 300, 50, "Play Again", font_medium):
            reset_korean_rps()
        if draw_button(screen, WIDTH - 140, HEIGHT - 60, 120, 40, "Menu", font_small):
            reset_korean_rps()
            return "menu"
        return

    # Display move selection images for player input
    moves = ['rock', 'paper', 'scissors']
    spacing = 200
    start_x = WIDTH//2 - spacing * 1.5
    images = [rock_img, paper_img, scissors_img]

    for i, move in enumerate(moves):
        img = images[i]
        x = start_x + i * spacing
        img_rect = img.get_rect(center=(x + 75, HEIGHT//2 + 50))
        screen.blit(img, img_rect)

        mouse_pos = pygame.mouse.get_pos()
        if img_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, YELLOW, img_rect.inflate(10, 10), 3, border_radius=5)
            if pygame.mouse.get_pressed()[0]:
                if click_sound:
                    click_sound.play()
                # Set the player's move from the selected option.
                player_move = move
                # Update the player's internal history (maxlen=10 as defined in the Player class)
                krps_player.record_move(player_move)
                # Now the AI uses the player's move_history (which now reflects prior moves)
                ai_move = krps_ai.make_move(krps_player.move_history)
                krps_ai.record_move(ai_move)
                # Also update your display deques (if you're keeping them for visual history)
                krps_player_history.append(player_move)
                krps_ai_history.append(ai_move)
                time.sleep(0.2)
                if stage == "initial":
                    outcome = rps_outcome(player_move, ai_move)
                    if outcome == "win":
                        attacker = 1
                        stage = "battle"
                    elif outcome == "lose":
                        attacker = 2
                        stage = "battle"
                    else:  # outcome is draw
                        player_move = None
                        ai_move = None  # Reset so the initial phase repeats
                else:
                    # For the battle stage, determine the final winner.
                    if player_move == ai_move:
                        final_winner = attacker
                    else:
                        attacker_move = player_move if attacker == 1 else ai_move
                        defender_move = ai_move if attacker == 1 else player_move
                        outcome = rps_outcome(attacker_move, defender_move)
                        if outcome == "lose":
                            attacker = 2 if attacker == 1 else 1

    #highlighting the most recent move
    def get_image(move):
        return rock_img if move == 'rock' else paper_img if move == 'paper' else scissors_img

    history_y = HEIGHT - 120
    label_font = font_small

    # Display player's move history
    player_history_label = label_font.render("You:", True, WHITE)
    screen.blit(player_history_label, (50, history_y))
    x_offset = 50 + player_history_label.get_width() + 10
    player_history = list(krps_player_history)[-3:]
    for index, move in enumerate(player_history):
        img = pygame.transform.smoothscale(get_image(move), (40, 40))
        screen.blit(img, (x_offset, history_y))
        # Highlight the most recent move (last in the list)
        if index == len(player_history) - 1:
            pygame.draw.rect(screen, YELLOW, (x_offset, history_y, 40, 40), 3)
        x_offset += 50

    # Display computer's move history
    comp_history_label = label_font.render("Computer:", True, WHITE)
    comp_label_x = WIDTH - 300
    screen.blit(comp_history_label, (comp_label_x, history_y))
    x_offset_comp = comp_label_x + comp_history_label.get_width() + 10
    comp_history = list(krps_ai_history)[-3:]
    for index, move in enumerate(comp_history):
        img = pygame.transform.smoothscale(get_image(move), (40, 40))
        screen.blit(img, (x_offset_comp, history_y))
        if index == len(comp_history) - 1:
            pygame.draw.rect(screen, YELLOW, (x_offset_comp, history_y, 40, 40), 3)
        x_offset_comp += 50

    if draw_button(screen, x=20, y=HEIGHT - 60, width=160, height=40, text="Back to Menu", font=font_small):
        reset_korean_rps()
        return "menu"

    return None

def draw_game():
    screen.fill((30, 30, 50))
    
    # Player scores display
    p1_score = font_medium.render(f"{game.player1.name}: {game.player1.score}", True, WHITE)
    p2_score = font_medium.render(f"{game.player2.name}: {game.player2.score}", True, WHITE)
    screen.blit(p1_score, (50, 30))
    screen.blit(p2_score, (WIDTH - 50 - p2_score.get_width(), 30))

    # Tournament status
    if game.tournament:
        remaining = font_small.render(
            f"Players remaining: {len(game.tournament.players) + len(game.tournament.winners)}", 
            True, WHITE
        )
        screen.blit(remaining, (WIDTH//2 - remaining.get_width()//2, 30))

    # Game area
    if game.player1_move and game.player2_move and game.is_animating():
        game.update_animation()
        progress = game.animation_frame / game.max_animation_frames

        # Animate player 1's choice
        if game.player1_move:
            img = rock_img if game.player1_move == 'rock' else paper_img if game.player1_move == 'paper' else scissors_img
            x = 150 * progress
            screen.blit(img, (x, HEIGHT//2 - img.get_height()//2))
        else:
            q = font_large.render("?", True, WHITE)
            screen.blit(q, (150 * progress, HEIGHT//2 - 25))

        # Animate player 2's choice
        if game.player2_move:
            img = rock_img if game.player2_move == 'rock' else paper_img if game.player2_move == 'paper' else scissors_img
            x = WIDTH - 150 * progress - img.get_width()
            screen.blit(img, (x, HEIGHT//2 - img.get_height()//2))
        else:
            q = font_large.render("?", True, WHITE)
            screen.blit(q, (WIDTH - 150 * progress - 50, HEIGHT//2 - 25))

        # VS text during animation
        if 0.3 < progress < 0.7:
            vs = font_large.render("VS", True, RED)
            screen.blit(vs, (WIDTH//2 - vs.get_width()//2, HEIGHT//2 - 25))
    else:
        if game.player1_move and game.player2_move:
            # Show final results
            img1 = rock_img if game.player1_move == 'rock' else paper_img if game.player1_move == 'paper' else scissors_img
            img2 = rock_img if game.player2_move == 'rock' else paper_img if game.player2_move == 'paper' else scissors_img
            
            screen.blit(img1, (150, HEIGHT//2 - img1.get_height()//2))
            screen.blit(img2, (WIDTH - 150 - img2.get_width(), HEIGHT//2 - img2.get_height()//2))
            
            # Result text
            if game.result == 'player1':
                result_text = font_large.render(f"{game.player1.name} wins!", True, GREEN)
            elif game.result == 'player2':
                result_text = font_large.render(f"{game.player2.name} wins!", True, GREEN)
            else:
                result_text = font_large.render("Draw!", True, YELLOW)
            screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, HEIGHT//2 - 175))
            
            # Next round button
            if draw_button(screen=screen,
                x=WIDTH//2 - 150,
                y=HEIGHT - 100,
                width=300,
                height=50,
                text="Next Match" if game.tournament else "Next Round",
                font=font_medium):
                if click_sound: click_sound.play()

                if game.tournament:
                    if game.result == 'draw':
                        time.sleep(0.2)
                        game.reset_round()
                    else:
                        winner = game.player1 if game.result == 'player1' else game.player2
                        if game.tournament.declare_winner(winner):
                            game.final_tournament_winner = winner
                            return "Congratulations"
                        elif game.next_tournament_match():  # Only now do we call this
                            time.sleep(0.2)
                            return None
                        else:
                            return "menu"
                else:
                    game.reset_round()
        else:
            # Image-based selection for human players
            if not game.player1_move and not game.player1.is_ai:
                select_text = font_medium.render(f"{game.player1.name}, choose your move:", True, WHITE)
                screen.blit(select_text, (WIDTH//2 - select_text.get_width()//2, 225))
                
                # Calculate positions for images
                spacing = 200
                start_x = (WIDTH//2 - spacing * 1.5) + 40
                images = [
                    (rock_img, start_x, 'rock'),
                    (paper_img, start_x + spacing, 'paper'),
                    (scissors_img, start_x + spacing * 2, 'scissors')
                ]
                
                for img, x, move in images:
                    img_rect = img.get_rect(center=(x + 75, HEIGHT//2 + 50))
                    screen.blit(img, img_rect)
                    
                    # Hover effect
                    mouse_pos = pygame.mouse.get_pos()
                    if img_rect.collidepoint(mouse_pos):
                        pygame.draw.rect(screen, YELLOW, img_rect.inflate(10, 10), 3, border_radius=5)
                        
                        # Handle click
                        if pygame.mouse.get_pressed()[0]:
                            if click_sound: click_sound.play()
                            game.make_move(1, move)
                            if game.player2.is_ai:
                                # AI makes move immediately after player
                                game.make_move(2, game.player2.make_move(game.player1.move_history))

            if not game.player2_move and not game.player2.is_ai:
                select_text = font_medium.render(f"{game.player2.name}, choose your move:", True, WHITE)
                screen.blit(select_text, (WIDTH//2 - select_text.get_width()//2, 100))

                
                # Calculate positions for images
                spacing = 150
                start_x = WIDTH//2 - spacing * 1.5
                images = [
                    (rock_img, start_x, 'rock'),
                    (paper_img, start_x + spacing, 'paper'),
                    (scissors_img, start_x + spacing * 2, 'scissors')
                ]
                
                for img, x, move in images:
                    img_rect = img.get_rect(center=(x + 75, HEIGHT//2 + 150))
                    screen.blit(img, img_rect)
                    
                    # Hover effect
                    mouse_pos = pygame.mouse.get_pos()
                    if img_rect.collidepoint(mouse_pos):
                        pygame.draw.rect(screen, YELLOW, img_rect.inflate(10, 10), 3, border_radius=5)
                        
                        # Handle click
                        if pygame.mouse.get_pressed()[0]:
                            if click_sound: click_sound.play()
                            game.make_move(2, move)
                            if game.player1.is_ai:
                                game.make_move(1, game.player1.make_move(game.player2.move_history))

            if game.player1.is_ai and game.player2.is_ai and game.result is None:
                move1 = game.player1.make_move(game.player2.move_history)
                move2 = game.player2.make_move(game.player1.move_history)
                game.make_move(1, move1)
                game.make_move(2, move2)
                time.sleep(1.0)  # Optional pause so we can see what happened

    # Quit button
    if draw_button(screen=screen,
                  x=WIDTH - 120,
                  y=HEIGHT - 60,
                  width=100,
                  height=40,
                  text="Quit",
                  font=font_small):
        if click_sound: click_sound.play()
        time.sleep(0.2)
        return "menu"
    
    return None

def draw_tournament_winner(winner):
    screen.blit(menu_bg, (0, 0))
    
    title = font_large.render("Tournament Winner!", True, YELLOW)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    winner_text = font_large.render(winner.name, True, GREEN)
    screen.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, 200))
    
    score_text = font_medium.render(f"Final Score: {winner.score}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 280))
    
    # Game history
    history_title = font_medium.render("Game History:", True, WHITE)
    screen.blit(history_title, (WIDTH//2 - history_title.get_width()//2, 350))
    
    for i, match in enumerate(game.game_history[-5:]):  # Show last 5 matches
        match_text = font_small.render(
            f"{match['player1']} ({match['move1']}) vs {match['player2']} ({match['move2']}): " +
            ("Draw" if match['result'] == 'draw' else f"{match['player1'] if match['result'] == 'player1' else match['player2']} wins"), 
            True, WHITE
        )
        screen.blit(match_text, (WIDTH//2 - match_text.get_width()//2, 400 + i*30))
    
    # Back to menu button
    if draw_button(screen, WIDTH//2 - 150, HEIGHT - 100, 300, 50, "Back to Menu", font_medium):
        if click_sound:
            click_sound.play()
        time.sleep(0.2)
        return "menu"
    
    return None

def draw_congratulations():
    screen.fill((30, 30, 60))

    title = font_large.render("Congratulations!", True, ORANGE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

    if game.final_tournament_winner:
        name = game.final_tournament_winner.name
        wins = game.final_tournament_winner.score

        winner_text = font_medium.render(f"{name} won the tournament!", True, GREEN)
        screen.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, 200))

        score_text = font_small.render(f"Total wins: {wins}", True, WHITE)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 250))

    if draw_button(screen, WIDTH//2 - 150, HEIGHT - 120, 300, 50, "Back to Menu", font_medium):
        if click_sound: click_sound.play()
        game.player1 = None
        game.player2 = None
        game.player1_move = None
        game.player2_move = None
        game.result = None
        game.tournament = None
        game.final_tournament_winner = None
        return "menu"

    return None

def rps_outcome(p1, p2):
    if p1 == p2:
        return "draw"
    elif (p1 == "rock" and p2 == "scissors") or \
         (p1 == "scissors" and p2 == "paper") or \
         (p1 == "paper" and p2 == "rock"):
        return "win"
    else:
        return "lose"
    
# Game variables
player_name = ""
tournament_names = ""
selected_difficulty = 1
double_choice_difficulty = 1
input_active = False
tournament_input_active = False
double_choice_stage = 0
player_choices = []
ai_choices = []
player_wins_double = 0
computer_wins_double = 0

# Korean RPS globals
player_final = None
ai_final = None
stage = "initial"
attacker = None 
round_winner = None
final_winner = None
player_move = None
ai_move = None
player_wins_korean = 0
computer_wins_korean = 0
is_win = False
krps_ai = None
krps_player = None
krps_player_history = deque(maxlen=3)
krps_ai_history = deque(maxlen=3)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    action = None
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if game_state == "single_player_menu":
                # Name input box
                if WIDTH//2 - 150 <= mouse_pos[0] <= WIDTH//2 + 150 and 220 <= mouse_pos[1] <= 260:
                    input_active = True
                else:
                    input_active = False
            
            elif game_state == "tournament_menu":
                # Names input box
                if WIDTH//2 - 250 <= mouse_pos[0] <= WIDTH//2 + 250 and 220 <= mouse_pos[1] <= 260:
                    tournament_input_active = True
                else:
                    tournament_input_active = False
            elif game_state == CONGRATULATIONS:
                action = draw_congratulations()
        
        if event.type == pygame.KEYDOWN:
            if input_active and game_state == "single_player_menu":
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode
            
            if tournament_input_active and game_state == "tournament_menu":
                if event.key == pygame.K_BACKSPACE:
                    tournament_names = tournament_names[:-1]
                else:
                    tournament_names += event.unicode
    
    # Drawing and button handling
    if game_state == MENU:
        action = draw_menu()
    elif game_state == "single_player_menu":
        action = draw_single_player_menu()
    elif game_state == "tournament_menu":
        action = draw_tournament_menu()
    elif game_state == DOUBLE_CHOICE:
        action = draw_double_choice_game()
    elif game_state == KOREAN_RPS:
        action = draw_korean_rps()
    elif game_state == PLAYING:
        action = draw_game()
    elif game_state == "tournament_winner":
        action = draw_tournament_winner(game.get_tournament_winner())
    elif game_state == "timer_menu":
        action = draw_timed_menu()
    elif game_state == TIMED_GAME:
        action = draw_timed_game()
    
    # Handle actions
    if action == "quit":
        running = False
    elif action == "menu":
        game_state = MENU
    elif action == "single_player_menu":
        game_state = "single_player_menu"
    elif action == "tournament_menu":
        game_state = "tournament_menu"
    elif action == "double_choice":
        game_state = DOUBLE_CHOICE
    elif action == "korean_rps":
        reset_korean_rps()
        game_state = KOREAN_RPS
    elif action == "congratulations":
        game_state = CONGRATULATIONS
    elif isinstance(action, tuple):
        if action[0] == "set_difficulty":
            selected_difficulty = action[1]
        elif action[0] == "start_single":
            game.start_single_player(action[1], action[2])
            game_state = PLAYING
        elif action[0] == "start_tournament":
            game.start_tournament(action[1])
            game_state = PLAYING
        elif action[0] == "start_timed":
            game.start_timed_game(action[1], action[2], action[3])
            game_state = TIMED_GAME
            countdown_active = True
            countdown_start_time = pygame.time.get_ticks()
            game_result = None
    elif action == "tournament_winner":
        game_state = "tournament_winner"
    elif action == "timer_menu":
        game_state = "timer_menu"
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()