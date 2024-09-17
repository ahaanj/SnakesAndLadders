import pygame
import random
import sys

# Pygame initialization
pygame.init()


SCREEN_WIDTH, SCREEN_HEIGHT = 820, 600 # Screen Dimensions 
CELL_SIZE = 50 # Size of each cell in the board 
BOARD_SIZE = 10 # Number of cells per row/column 
MAX_VAL = BOARD_SIZE * BOARD_SIZE # Max value on the board 
DICE_SIZE = 100 # Size of the dice 

# Load in png of board and Snakes and Ladders logo
bg = pygame.image.load("bg.png") 
logo = pygame.image.load("sl.png")

# Function to generate random positions of ladders
def generate_ladders_position():
    ladders_list = [] # List to store the ladder positions 
    for i in range(14): # Generate 14 ladders
        updating = True
        while updating:
            pos = random.randint(5, 85) # Range for random position generation of ladders
            if pos not in ladders_list and pos - 15 not in ladders_list:
                if pos + 15 not in ladders_list:
                    ladders_list.append(pos) # Add ladder if position satisfies conditions 
                    updating = False
    print(ladders_list)
    return ladders_list

# Function to geneare random positions of snakes 
def generate_snakes_position(ladders_list):
    snakes_list = [] # List to store the snake positions 
    for i in range(10): # Generate 10 snakes 
        updating = True
        while updating:
            pos = random.randint(20, 95) # Range for random position generation of snakes 
            pos1 = pos - 10
            if pos not in snakes_list and pos + 10 not in snakes_list:
                if pos - 10 not in snakes_list:
                    if pos not in ladders_list and pos - 10 not in ladders_list:
                        if pos + 15 not in ladders_list and pos + 5 not in ladders_list:
                            snakes_list.append(pos)
                            updating = False
    print(snakes_list)
    return snakes_list

# Assign colors to RGB 
WHITE = (255, 255, 255) # Color for drawing text and dice
BG_GREEN = (153, 232, 137) # Background color for the screen 
BLACK = (0, 0, 0) # Color for drawing ladders and text
RED = (255, 0, 0) # Color for drawing snakes 
BLUE = (0, 0, 255) # Color assigned to second player 
YELLOW = (255, 255, 0) # Color assigned to first player 
BUTTON_COLOR = (0, 200, 0) # Color for the restart button 
BUTTON_HOVER_COLOR = (0, 255, 0) # Color for when cursor hovers


FONT = pygame.font.Font(None, 36) # Default font with size 36

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake and Ladder Game")

# Function to retrieve player names
def get_players_list():
    name_list = [] # List to store player names
    for i in range(1, 3): # Loop for 2 players
        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20, 200, 40)  # Input box for player name
        color_inactive = pygame.Color('grey')  # Color when input box is inactive
        color_active = pygame.Color('blue') # Color when input box is active
        color = color_inactive
        active = False # Flag to check if input box is active
        text = ''
        done = False

        while not done:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: # Quit the game
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN: # Check for mouse click
                    if input_box.collidepoint(event.pos): # check if click is within input box
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN: # check for key press
                    if active:
                        if event.key == pygame.K_RETURN: # End input upon Enter key 
                            done = True
                        elif event.key == pygame.K_BACKSPACE: # Remove last character on Backspace
                            text = text[:-1]
                        else:
                            text += event.unicode  # Add typed character to text

            screen.fill(BG_GREEN) # Clear screen with background color
            prompt_surface = FONT.render(f"Enter name for Player {i}:", True, BLACK) # Prompt for player name
            screen.blit(prompt_surface, (SCREEN_WIDTH // 2 - prompt_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
            txt_surface = FONT.render(text, True, color) # Render entered text
            width = max(200, txt_surface.get_width() + 10) # Adjust input box width
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color, input_box, 2) # Draw input box

            pygame.display.flip() # Update display 
        name_list.append(text) # Add entered name to list 
    return name_list

# Function to get row and column number from cell number
def get_cell_num(cell):
    row = cell // 10 # Calculate row number
    col = 0
    if row % 2 == 0:
        col = cell - row*10 # Calculate column number for even row
    else:
        col = 9 - (cell - row*10) # Calculate column number for odd row
    return row, col

# Function to draw the game board
def draw_board(ladders_list, snakes_list, player_name, dice_value, position, player_color):
    screen.fill(BG_GREEN) # Clear screen with background color
    screen.blit(bg, (0,0))  # Draw background image
    screen.blit(logo, (400,0)) # Draw logo image
    
    draw_dice(dice_value) # Draw dice with current value

    player_action = FONT.render(f"{player_name}'s turn", True, player_color) # Show current player's turn
    screen.blit(player_action, (550, SCREEN_HEIGHT // 2 + 120))

    player_pos = FONT.render(f"{player_name}'s position: {position}", True, player_color) # Show current player's position
    screen.blit(player_pos, (550, SCREEN_HEIGHT // 2 + 80))

    # Draw snakes
    for start in snakes_list:
        start_row, start_col = get_cell_num(start - 1) # Get start cell row and column
        end_row, end_col = get_cell_num(start - 10 - 1) # Get end cell row and column
        start_row = BOARD_SIZE - 1 - start_row
        end_row = BOARD_SIZE - 1 - end_row
        # Draw the snake as a red line
        pygame.draw.line(screen, RED, 
                         (start_col * CELL_SIZE + CELL_SIZE // 2, start_row * CELL_SIZE + CELL_SIZE // 2),
                         (end_col * CELL_SIZE + CELL_SIZE // 2, end_row * CELL_SIZE + CELL_SIZE // 2), 5) # Draw snake
     
    # Draw ladders
    for start in ladders_list:
        start_row, start_col = get_cell_num(start - 1) # Get start cell row and column
        end_row, end_col = get_cell_num(start + 15 - 1) # Get end cell row and column
        start_row = BOARD_SIZE - 1 - start_row
        end_row = BOARD_SIZE - 1 - end_row
        # Draw the ladder as a black line
        pygame.draw.line(screen, BLACK, 
                         (start_col * CELL_SIZE + CELL_SIZE // 2, start_row * CELL_SIZE + CELL_SIZE // 2),
                         (end_col * CELL_SIZE + CELL_SIZE // 2, end_row * CELL_SIZE + CELL_SIZE // 2), 5)  # Draw ladder
    # Draw roll button  
    button = pygame.Surface((100, 100))  # Create a surface for the button
    pygame.draw.rect(button, BLACK, (0, 0, 100, 100), 5)  # Draw the button rectangle
    text_surface = FONT.render("ROLL", True, WHITE)  # Render the button text
    screen.blit(button, (560, 480)) # Draw the button on the screen
    screen.blit(text_surface, (576, 515)) # Draw the text on the button
    
    pygame.display.flip() # Update display

# Function to draw players on the board
def draw_players(positions, colors):
    for player_name, position in positions.items():
        if position == 0:
            continue # Skip drawing if the player is at the starting position
        player_row, player_col = get_cell_num(position - 1) # Get player cell row and column
        player_row = BOARD_SIZE - 1 - player_row
         # Draw the player as a circle
        pygame.draw.circle(screen, colors[player_name], 
                           (player_col * CELL_SIZE + CELL_SIZE // 2, player_row * CELL_SIZE + CELL_SIZE // 2), 15) # Draw the player 
        
# Function to draw the dice with the current value
def draw_dice(dice_value):
    dice_surface = pygame.Surface((DICE_SIZE, DICE_SIZE)) # Create a surface for the dice
    dice_surface.fill(WHITE) # Fill the surface with white color
    pygame.draw.rect(dice_surface, BLACK, (0, 0, DICE_SIZE, DICE_SIZE), 5) # Draw the dice border
    
    # Draw dots on the dice based on the value
    if dice_value == 1 or dice_value == 3 or dice_value == 5: # If the dice value is 1, 3, or 5, draw the center dot 
        pygame.draw.circle(dice_surface, BLACK, (DICE_SIZE // 2, DICE_SIZE // 2), 10)
    if dice_value >= 2: # If the dice value is 2 or more, draw the two diagonal corner dots
        pygame.draw.circle(dice_surface, BLACK, (DICE_SIZE // 4, DICE_SIZE // 4), 10)
        pygame.draw.circle(dice_surface, BLACK, (3 * DICE_SIZE // 4, 3 * DICE_SIZE // 4), 10)
    if dice_value >= 4: # If the dice value is 4 or more, draw the two remaining corner dots
        pygame.draw.circle(dice_surface, BLACK, (3 * DICE_SIZE // 4, DICE_SIZE // 4), 10)
        pygame.draw.circle(dice_surface, BLACK, (DICE_SIZE // 4, 3 * DICE_SIZE // 4), 10)
    if dice_value == 6: # If the dice value is 6, draw the two additional center vertical dots
        pygame.draw.circle(dice_surface, BLACK, (DICE_SIZE // 4, DICE_SIZE // 2), 10)
        pygame.draw.circle(dice_surface, BLACK, (3 * DICE_SIZE // 4, DICE_SIZE // 2), 10)
     # Draw the dice on the screen
    screen.blit(dice_surface, (SCREEN_WIDTH - DICE_SIZE - 20, SCREEN_HEIGHT - DICE_SIZE - 20))

# Function to roll the dice
def roll_dice():
    return random.randint(1, 6) # Returns a random dice value between 1 and 6

# Function to check if the player lands on a ladder
def check_for_ladder(position, ladders_list, player_name):
    if position in ladders_list:
        position += 15 # Move the player up the ladder
        msg = f'{player_name} climbed a ladder to {position}!' # Message to display and inform of ladder
        return position, msg
    return position, None  
     
# Function to check if the player lands on a snake
def check_for_snake(position, snakes_list, player_name):
    if position in snakes_list:
        position -= 10  # Move the player down the snake
        msg = f'{player_name} fell down a snake to {position}!' # Message to display and inform of snake
        return position, msg
    return position, None 

# Function to display if snake or ladder has been hit on the screen
def show_message(msg):
    # Clear the previous message area
    text_surface = FONT.render(msg, True, BLACK) # Render the message text
    text_rect = text_surface.get_rect(midleft=(100, 577)) # Position the message text
    pygame.draw.rect(screen, BG_GREEN, text_rect)  # Clear the previous message area
    screen.blit(text_surface, text_rect) # Draw the new message
    pygame.display.flip() # Update the display 

# Function to draw the restart button
def draw_restart_button():
    button_rect = pygame.Rect(550, 300, 200, 60)  # Create a rectangle for the button
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)  # Draw the button rectangle
    text_surface = FONT.render("Restart", True, WHITE)  # Render the button text
    text_rect = text_surface.get_rect(center=button_rect.center)  # Center the text on the button
    screen.blit(text_surface, text_rect)  # Draw the text on the button
    pygame.display.flip()  # Update the display
    return button_rect  # Return the button rectangle

# Main game function
def main():
    name_list = get_players_list()  # Get the list of player names
    colors = {name_list[0]: YELLOW, name_list[1]: BLUE}  # Assign colors to players Yellow and Blue
    print(name_list)  # Print the player names 
    screen.fill(WHITE)  # Fill the screen with white color
    ladders_list = generate_ladders_position()  # Generate the positions of ladders
    snakes_list = generate_snakes_position(ladders_list)  # Generate the positions of snakes
    positions = {name_list[0]: 0, name_list[1]: 0}  # Initialize player positions
    current_player = 0  # Variable to track the current player's turn
    # Draw the initial board
    draw_board(ladders_list, snakes_list, name_list[current_player], 1, 0, colors[name_list[current_player]])
    draw_players(positions, colors)  # Draw the initial player positions
    draw_dice(1)  # Draw the initial dice
    pygame.display.flip()  # Update the display

    game_over = False  # Track if the game is over
    while True:
        roll = False  # Track if the roll button is clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check if the quit event is triggered
                pygame.quit()  # Quit pygame
                sys.exit()  # Exit the program
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check if the mouse button is clicked
                mouse = pygame.mouse.get_pos()  # Retrieve the mouse position
                if 560 <= mouse[0] <= 660 and 480 <= mouse[1] <= 580:  # Check if the roll button is clicked
                    roll = True
                if game_over and restart_button.collidepoint(mouse):  # Check if the restart button is clicked
                    main()  # Restart the game

        if roll and not game_over:
            player_name = name_list[current_player]
            position = positions[player_name]
            dice_value = roll_dice()  # Roll the dice
            new_position = position + dice_value  # Calculate the new position
            if new_position > 100:  # Ensure the position does not exceed 100
                new_position = 100

            # Check if the player lands on a ladder
            new_position, ladder_msg = check_for_ladder(new_position, ladders_list, player_name)
            # Check if the player lands on a snake
            new_position, snake_msg = check_for_snake(new_position, snakes_list, player_name)
            positions[player_name] = new_position  # Update the player's position

            # Draw the updated board and player positions
            draw_board(ladders_list, snakes_list, player_name, dice_value, new_position, colors[player_name])
            draw_players(positions, colors)

            if ladder_msg:
                show_message(ladder_msg)  # Show the ladder message
            elif snake_msg:
                show_message(snake_msg)  # Show the snake message
            else:
                show_message("")  # Clear the message if no ladder or snake

            if new_position == 100:  # Check if the player wins
                show_message(f"{player_name} won the game!")  # Show the win message
                pygame.display.flip()
                pygame.time.delay(1000)  # Wait for 1 second
                restart_button = draw_restart_button()  # Draw the restart button
                game_over = True  # Set the game over flag

            current_player = (current_player + 1) % 2  # Switch to the next player

        pygame.display.flip()  # Ensure the display is updated with the latest drawings

if __name__ == "__main__":
    main()  # Start the game