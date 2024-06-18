from tkinter import Tk, Button
import random

# Define game board and current player
board = [' ' for _ in range(9)]
current_player = 'X'


def main(whose,ai):
   # Function to check if a player has won
   def check_winner():
     winning_conditions = [
         (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
         (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
         (0, 4, 8), (2, 4, 6)              # Diagonals
     ]
     for row in winning_conditions:
       if board[row[0]] == board[row[1]] == board[row[2]] != ' ':
         return board[row[0]]
     return None

   # Function to check if the board is full (tie)
   def check_board_full():
     for cell in board:
       if cell == ' ':
         return False
     return True

   #get available moves
   def get_available_moves(board):
       # Get a list of available moves (empty cells) on the board
       return [(row, col) for row in range(1,4) for col in range(3) if board[row * 3 + col - 3] == " "] 

   #ai easy
   def ai_easy():
      def ai_move(board, buttons):  # Pass buttons list as argument
       available_moves = get_available_moves(board)
       chosen_move = random.choice(available_moves)
       row, col = chosen_move
       board_index = row * 3 + col - 3
       board[board_index] = 'O'  # Update board with 'O' at chosen move

      #Update button text and color
       buttons[board_index].config(text='O', fg='red')  # Set O mark with red color

      ai_move(board, buttons)  # Pass buttons list during function call
      show_message(f"Player {current_player}'s turn")

   def ai_hard(board, buttons):
    # Function to evaluate the board for the AI player (maximizing score)
    def evaluate(board):
        scores = {'X': 1, 'O': -1, ' ': 0}
        # Check rows, columns, and diagonals
        lines = [
            [board[0], board[1], board[2]],
            [board[3], board[4], board[5]],
            [board[6], board[7], board[8]],
            [board[0], board[3], board[6]],
            [board[1], board[4], board[7]],
            [board[2], board[5], board[8]],
            [board[0], board[4], board[8]],
            [board[2], board[4], board[6]],
        ]
        
        player_score = 0
        opponent_score = 0
        for line in lines:
            if line == ['X', 'X', 'X']:
                return 1000  # High positive score for winning line
            if line == ['O', 'O', 'O']:
                return -1000  # High negative score for opponent's winning line
            player_score += line.count('X') * scores['X']
            opponent_score += line.count('O') * scores['O']
        
        return player_score + opponent_score

    # Function to find the best move for the AI
    def find_best_move(board, maximizing_player):
        best_score = -float('inf') if maximizing_player else float('inf')
        best_move = None
        available_moves = get_available_moves(board)
        
        for move in available_moves:
            row, col = move
            index = (row - 1) * 3 + col - 1  # Convert 1-based to 0-based index
            board[index] = 'X' if maximizing_player else 'O'  # Simulate move
            score = minimax(board, 0, not maximizing_player)  # Evaluate score using minimax
            board[index] = ' '  # Undo simulated move
            
            if maximizing_player and score > best_score:
                best_score = score
                best_move = move
            elif not maximizing_player and score < best_score:
                best_score = score
                best_move = move
        
        return best_move

    # Minimax algorithm to evaluate the best score
    def minimax(board, depth, maximizing_player):
        score = evaluate(board)
        if abs(score) == 1000 or not get_available_moves(board):
            return score
        
        if maximizing_player:
            max_eval = -float('inf')
            for move in get_available_moves(board):
                row, col = move
                index = (row - 1) * 3 + col - 1
                board[index] = 'X'
                eval = minimax(board, depth + 1, False)
                board[index] = ' '
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in get_available_moves(board):
                row, col = move
                index = (row - 1) * 3 + col - 1
                board[index] = 'O'
                eval = minimax(board, depth + 1, True)
                board[index] = ' '
                min_eval = min(min_eval, eval)
            return min_eval

    # Function to get available moves
    def get_available_moves(board):
        return [(row, col) for row in range(1, 4) for col in range(1, 4) if board[(row - 1) * 3 + (col - 1)] == ' ']

    # Function to update button text and color
    def update_button(board_index, player):
        buttons[board_index].config(text=player, fg='red' if player == 'O' else 'blue')

    # AI makes the best move and updates the board and UI
    best_move = find_best_move(board, True)
    if best_move:
        row, col = best_move
        board_index = (row - 1) * 3 + (col - 1)
        board[board_index] = 'O'
        update_button(board_index, 'O')
        show_message(f"Player {current_player}'s turn")

    return board

 



   # Function to handle button click
   def button_click(button_number):
     global current_player, board
     if board[button_number] == ' ':
       board[button_number] = current_player
       if current_player == 'X':
         buttons[button_number].config(text='X', fg='blue')  # Set X mark with blue color
       else:
         buttons[button_number].config(text='O', fg='red')   # Set O mark with red color
       winner = check_winner()
       if winner:
         # Declare winner and disable buttons
         show_message(f"Player {winner} wins!")
         disable_buttons()
       elif check_board_full():
         # Declare tie and disable buttons
         show_message("It's a tie!")
         disable_buttons()
       else:
         # Switch player
         if ai==1:
           show_message(f"AI's turn")
           ai_easy()
           aip_win()
         elif ai==2:
           show_message(f"AI's turn")
           ai_hard(board,buttons)
           aip_win()
         else:
           current_player = 'X' if current_player == 'O' else 'O'
           show_message(f"Player {current_player}'s turn")
         
   #checking winner for ai
   def aip_win():
     winner = check_winner()
     if winner:
       # Declare winner and disable buttons
       show_message(f"Player {winner} wins!")
       disable_buttons()
     elif check_board_full():
       # Declare tie and disable buttons
       show_message("It's a tie!")
       disable_buttons()


   # Function to disable buttons after game ends
   def disable_buttons():
     for button in buttons:
       button.config(state='disabled')

   # Function to show message
   def show_message(message):
     message_label.config(text=message)

   # Function to restart the game
   def restart_game():
     global board, current_player
     board = [' ' for _ in range(9)]
     current_player = 'X'
     show_message(f"Player {current_player}'s turn")
     for button in buttons:
       button.config(text=' ', state='normal', fg='black')  # Reset button text, state, and color

   # Create the main window


   window = Tk()
   window.title("Tic Tac Toe")

   # Create a label for current player
   message_label = Button(window, text=f"Player {current_player}'s turn", font=('Arial', 16), state='disabled')
   message_label.grid(row=0, column=0, columnspan=4)

  # Create buttons for the game board
   buttons = []
   for row in range(1, 4):
     for col in range(3):
       button_number = row * 3 + col - 3
       button_text = Button(window, text=' ', font=('Arial', 24), width=3, height=1, command=lambda btn_num=button_number:     button_click(btn_num))
       button_text.grid(row=row, column=col)
       buttons.append(button_text)

   # player button
   
   who=Button(window, text=whose, font=('Arial', 12), command=restart_game, state="disabled")
   who.grid(row=5, column=0, columnspan=4)

   # Create a restart button
   restart_button = Button(window, text="Restart", font=('Arial', 12), command=restart_game)
   restart_button.grid(row=6, column=1)
   window.mainloop()

# Run the main loop
def entry():
  print("1. Both Players \n2. AI")
  en=int(input())
  if(en==2):
    print("1. Normal \n2. Hard")
    en=int(input())
    if en>0 & en<3:
     whose="Player V/S AI"
    main(whose,en)
  else:
    whose="Player V/S Player"
    main(whose,0)
    

entry()
 
      




