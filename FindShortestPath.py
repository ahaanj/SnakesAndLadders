def find_shortest_path(ladders, snakes):
    # Board is split into 100 cells (1 to 101)
    board = list(range(101))
    
    # Turn the value for the cells at the start of the ladders to the cells at the end, as 
    # that is where the player will end up.
    for start, end in ladders.items():
        board[start] = end

    # Turn the value for the cells at the start of the snakes to the cells at the end, as 
    # that is where the player will end up.
    for start, end in snakes.items():
        board[start] = end

    # Start the path list with 1, as that is the starting position for each player
    path = [1]
    # The player starts at 1, so we set the current position to 1
    position = 1

    # While the player has not completed the game
    while position < 100:
        # The minimum distance is a 6, as that is what is achievable with one roll
        min_dice_roll = 6
        # Create a "next_position" variable to compare with the current position
        next_position = position

        # Try each dice roll from 1-6
        for dice_roll in range(1, 7):
            # Calculate the new position after this roll
            new_position = position + dice_roll
            # Check if this new position is on the board and better than the last try
            if new_position <= 100 and board[new_position] > board[next_position]:
                # Update next_position with the new position after the best roll so far
                next_position = new_position
                # Set the minimum roll to the current roll
                min_dice_roll = dice_roll

        # Update the position of the player
        position = board[next_position]
        # Add the new position to the total path
        path.append(position)
    # Return the total shortest path from start to finish as found by the algorithm
    return path

# Define snake positions (where they start and where they end)
snakes = {8: 4, 18: 1, 26: 10, 39: 5, 51: 6, 54: 36, 56: 1, 60: 23, 
          75: 28, 83: 45, 85: 59, 90: 48, 92: 25, 97: 87, 99: 63}

# Define ladder positions (where they start and where they end)
ladders = {3: 20, 6: 14, 11: 28, 15: 34, 17: 74, 22: 37, 38: 59, 
           49: 67, 57: 76, 61: 78, 73: 86, 81: 98, 88: 91}

# Call the function to calculate the shortest path using the snakes and ladders provided
path = find_shortest_path(ladders, snakes)
print(path)