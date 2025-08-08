# Import modules
import random
import curses
import sys
from time import sleep

# Start screen
screen = curses.initscr()

# Hide cursor
curses.curs_set(0)

# Get height & width
screen_height = screen.getmaxyx()[0]
screen_width = screen.getmaxyx()[1]

# Create new window
window = curses.newwin(screen_height, screen_width, 0, 0)

# Allow window to accept keyboard input
window.keypad(1)

# Set the delay
window.timeout(125)

# Set initial position for snake head
snk_x = screen_width // 4
snk_y = screen_height // 2

# Set initial position for snake body
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x - 1], 
    [snk_y, snk_x - 2]
]

# Put food at middle of the screen
food = [screen_height // 2, screen_width // 2]

# Make food like a PI character
window.addch(food[0], food[1], curses.ACS_PI)

# Make initial movement to the right
current_key = curses.KEY_RIGHT

# Main loop
while True:
    # get next key from the user
    next_key = window.getch()
    
    # Check if the user pressed the key otherwise the key remains the same
    if next_key == -1:
        current_key = current_key
    else:
        current_key = next_key

    # Check if the snake collided with itself or with the walls to close the game
    if snake[0][0] in [0, screen_height] or snake[0][1] in [0, screen_width] or snake[0] in snake[1:]:
        curses.beep()
        print("Sorry You lose")
        sleep(5)
        sys.exit(0)

    # Make a new head for the snake
    new_head = [snake[0][0], snake[0][1]]

    # Check which key was pressed
    if current_key == curses.KEY_DOWN:
        new_head[0] += 1
    elif current_key == curses.KEY_UP:
        new_head[0] -= 1
    elif current_key == curses.KEY_RIGHT:
        new_head[1] += 1
    elif current_key == curses.KEY_LEFT:
        new_head[1] -= 1
    else:
        new_head = new_head

    # Insert it to the first place of snake list
    snake.insert(0, new_head)

    # Check if snake ate the food
    if snake[0] == food:
        # Remove food
        food = None
        # While food is removed generate new food to be replaced in a new place
        while food is None:
            new_food = [
                random.randint(2, screen_height - 2),
                random.randint(2, screen_width - 2)
            ]
            # Check if food is not on the snake's body
            if new_food not in snake:
                food = new_food
            else:
                food = None
        # Generate new food on the screen
        window.addch(food[0], food[1], curses.ACS_PI)
    
    # If snake didn't eat the food remove last segment of its body
    else:
        tail = snake.pop()
        window.addch(tail[0], tail[1], ' ')

    # Update snake position on the screen
    window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)