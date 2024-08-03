import os
import random
import praw

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    username=os.getenv('REDDIT_USERNAME'),
    password=os.getenv('REDDIT_PASSWORD'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)

game_board = [0, 1, 2, 3, 4, 5, 6, 7, 8]

winning_combos = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

def game_init():
    return "I accept your challenge. Be prepared to meet your maker. Your move.\n\nHere is an empty game board:\n\n" + display_board()

def display_board():
    board_str = ""
    for i, position in enumerate(game_board):
        board_str += f"[{position}] "
        if (i + 1) % 3 == 0:
            board_str += "\n"
    return board_str

def validate_move(player_move):
    if player_move and len(player_move) == 3:
        if player_move[0].isdigit():
            player_position = int(player_move[0])
            if player_position in range(9) and isinstance(game_board[player_position], int):
                if player_move[1] == '-' and player_move[2].upper() == 'X':
                    return True, ""
                return False, "Please separate your position choice and letter with a dash (-), and choose X for your letter."
            return False, f"Position {player_position} is already taken or out of range. Please pick another."
        return False, "The first character in your move should be a number."
    return False, "The move format is incorrect or the move is empty."

def update_game_board(player_position, letter):
    player_position = int(player_position)
    game_board[player_position] = letter.upper()

def make_a_move():
    while True:
        random_position = random.randint(0, 8)
        if isinstance(game_board[random_position], int):
            game_board[random_position] = 'O'
            break

def check_if_winner(player):
    for combo in winning_combos:
        if all(game_board[position] == player for position in combo):
            return True
    return False

def check_if_tie():
    return all(not isinstance(pos, int) for pos in game_board)

print(game_init())

subreddit = reddit.subreddit("testingground4bots")
for comment in subreddit.stream.comments(skip_existing=True):
    if comment.body.lower().startswith("move"):
        user_input = comment.body.split()[1]
        is_valid, error_msg = validate_move(user_input)
        
        if is_valid:
            update_game_board(user_input[0], user_input[2])
            response = "Your move:\n\n" + display_board()
            
            if check_if_winner('X'):
                response += "\nCongrats, you've beat me. Well played."
            elif check_if_tie():
                response += "\nWe've tied. Good game."
            else:
                make_a_move()
                response += "\nMy move:\n\n" + display_board()
                
                if check_if_winner('O'):
                    response += "\nHaha, I've won. Better luck next time."
                elif check_if_tie():
                    response += "\nWe've tied. Good game."
        else:
            response = f"Invalid move: {error_msg}"
        
        comment.reply(response)
