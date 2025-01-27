# File Name: AKavaleuskiy_CO1417

# Author Name: Aleksander Kavaleuskiy - G21251410 - AKavaleuskiy@Uclan.ac.uk
# Description: A challenging endless runner game where you control a dinosaur that must jump over
# cactuses to survive. Press SPACE to jump, P to pause, and R to restart. Try to beat your high score!


from tkinter import *
import random
import math

# Window dimensions and configuration
WIDTH = 800
HEIGHT = 600

# Create and configure main window with professional styling
win = Tk()
win.title('Dino Run - SPACE: Jump | P: Pause | R: Restart')
win.configure(bg='#2F4F4F')  # Dark slate gray background
win.resizable(False, False)  # Lock window size for consistent experience

canvas = Canvas(win, width=WIDTH, height=HEIGHT)
canvas.pack()
canvas.config(bg='#87CEEB')  # Sky blue background

# Game parameters and state variables
DELAY = 16  # Reduced delay for smoother animation (approximately 60 FPS)
Dino_frames = []  # Animation frames for dinosaur
GRAVITY = 0.8  # Gravity constant for more realistic jumps
INITIAL_JUMP_VELOCITY = -16  # Initial jump velocity
MAX_JUMP_HEIGHT = 200  # Maximum jump height
dino_velocity_y = 0  # Current vertical velocity
Score = 0
game_paused = False
game_over_state = False

# Animation control variables
frame_index = 0
in_a_jump = False
jump_start_y = HEIGHT - 75  # Starting Y position for jumps

# Load game assets with proper error handling
try:
    ground_image = PhotoImage(file='Directory/ground.png_')
    cloud_image = PhotoImage(file='Directory/cloud.png')
    Small_cactus_image = PhotoImage(file='Directory/cactus-small.png')
    Big_cactus_image = PhotoImage(file='Directory/cactus-big.png_')
    Small_cactus_image1 = PhotoImage(file='Directory/cactus-small.png')

    # Load dinosaur animation frames
    for i in range(4):
        Dino_frames.append(PhotoImage(file=f'Directory/dino{i}.png'))
    Dino_eye_image = PhotoImage(file="Directory/dino4.png")
except TclError:
    print("Error: Could not load game assets. Please check file paths.")
    exit(1)

# Create game objects with precise positioning
ground_obj = canvas.create_image(WIDTH / 2, HEIGHT, image=ground_image)
cloud_obj = canvas.create_image(WIDTH, cloud_image.height() / 2, image=cloud_image)
cloud_obj_2 = canvas.create_image(WIDTH / 2, cloud_image.height() / 2 + 18, image=cloud_image)
cloud_obj_3 = canvas.create_image(WIDTH / 3, cloud_image.height() / 2 + 40, image=cloud_image)
cloud_obj_4 = canvas.create_image(WIDTH / 1.5, cloud_image.height() / 2 + 65, image=cloud_image)
small_cactus_obj = canvas.create_image(WIDTH / 2, HEIGHT - 75, image=Small_cactus_image)
small_cactus_obj1 = canvas.create_image(WIDTH / 0.5, HEIGHT - 75, image=Small_cactus_image)
big_cactus_obj = canvas.create_image(WIDTH, HEIGHT - 75, image=Big_cactus_image)


def reset_game():
    """Reset all game variables and objects to initial state"""
    global Score, game_over_state, in_a_jump, dino_velocity_y, frame_index
    Score = 0
    game_over_state = False
    in_a_jump = False
    dino_velocity_y = 0
    frame_index = 0

    # Reset object positions
    canvas.coords(dino_obj, 100, HEIGHT - 75)
    canvas.coords(small_cactus_obj, WIDTH, HEIGHT - 75)
    canvas.coords(small_cactus_obj1, WIDTH * 1.5, HEIGHT - 75)
    canvas.coords(big_cactus_obj, WIDTH * 2, HEIGHT - 75)

    # Clear game over text and reset dinosaur image
    canvas.delete("game_over")
    canvas.itemconfig(dino_obj, image=Dino_frames[0])
    canvas.itemconfig(score_text, text="Score: 0")

    # Restart game loops
    update()
    dino_animation(0)


def dino_animation(frame_index):
    """Handle dinosaur running animation"""
    if not game_over_state and not game_paused:
        # Only animate when not jumping
        if not in_a_jump:
            canvas.itemconfig(dino_obj, image=Dino_frames[frame_index])
            frame_index = (frame_index + 1) % len(Dino_frames)
        win.after(100, dino_animation, frame_index)


def toggle_pause(event):
    """Toggle game pause state"""
    global game_paused
    game_paused = not game_paused
    if not game_paused:
        update()
        dino_animation(frame_index)
        canvas.itemconfig(pause_text, state='hidden')
    else:
        canvas.itemconfig(pause_text, state='normal')


def check_collision(dino_coords, obstacle_coords, obstacle_image):
    """Improved collision detection with precise hitbox"""
    # Add small padding to make collision feel more natural
    padding = 15
    dino_width = Dino_frames[0].width() - padding * 2
    dino_height = Dino_frames[0].height() - padding * 2

    return (obstacle_coords[0] - padding <= dino_coords[0] + dino_width / 2 and
            obstacle_coords[0] + obstacle_image.width() - padding >= dino_coords[0] - dino_width / 2 and
            obstacle_coords[1] - padding <= dino_coords[1] + dino_height / 2 and
            obstacle_coords[1] + obstacle_image.height() - padding >= dino_coords[1] - dino_height / 2)


def update():
    """Main game update loop"""
    global in_a_jump, dino_velocity_y, Score, game_over_state

    if game_paused:
        win.after(DELAY, update)
        return

    Score += 1
    canvas.itemconfig(score_text, text='Score: ' + str(Score))

    dino_cords = canvas.coords(dino_obj)
    small_cactus_cords = canvas.coords(small_cactus_obj)
    small_cactus_cords1 = canvas.coords(small_cactus_obj1)
    big_cactus_cords = canvas.coords(big_cactus_obj)

    # Enhanced collision detection
    if (check_collision(dino_cords, small_cactus_cords, Small_cactus_image) or
            check_collision(dino_cords, small_cactus_cords1, Small_cactus_image) or
            check_collision(dino_cords, big_cactus_cords, Big_cactus_image)):
        game_over()
        return False

    # Ground movement with smooth scrolling
    (x, y) = canvas.coords(ground_obj)
    if x > -99.55:
        canvas.move(ground_obj, -10, 0)
    else:
        canvas.move(ground_obj, WIDTH, 0)

    # Parallax cloud movement for depth effect
    for cloud, speed in [(cloud_obj, -2), (cloud_obj_2, -3), (cloud_obj_3, -1.5), (cloud_obj_4, -1)]:
        (x, y) = canvas.coords(cloud)
        if x >= -cloud_image.width():
            canvas.move(cloud, speed, 0)
        else:
            canvas.move(cloud, WIDTH + cloud_image.width(), 0)

    # Obstacle movement with varied speeds and better spacing
    base_speed = -8 - (Score / 1000)  # Gradually increase difficulty
    for cactus, speed_mult in [(small_cactus_obj, 1.2), (big_cactus_obj, 1.0), (small_cactus_obj1, 1.1)]:
        (x, y) = canvas.coords(cactus)
        if x >= -Small_cactus_image.width():
            canvas.move(cactus, base_speed * speed_mult, 0)
        else:
            random_pos = WIDTH + random.randrange(int(0.5 * WIDTH), int(WIDTH))
            canvas.coords(cactus, random_pos, y)

    # Physics-based jump mechanics
    if in_a_jump:
        # Apply gravity
        dino_velocity_y += GRAVITY

        # Update position
        new_y = dino_cords[1] + dino_velocity_y

        # Check ground collision
        if new_y >= jump_start_y:
            new_y = jump_start_y
            dino_velocity_y = 0
            in_a_jump = False

        # Update dinosaur position
        canvas.coords(dino_obj, dino_cords[0], new_y)

    win.after(DELAY, update)


def jump(event):
    """Handle jump input with improved physics"""
    global in_a_jump, dino_velocity_y
    if not in_a_jump and not game_paused and not game_over_state:
        in_a_jump = True
        dino_velocity_y = INITIAL_JUMP_VELOCITY
        # Use a different dinosaur frame for jump
        canvas.itemconfig(dino_obj, image=Dino_frames[2])


def game_over():
    """Handle game over state"""
    global game_over_state
    game_over_state = True
    canvas.itemconfig(dino_obj, image=Dino_eye_image)

    # Create game over overlay with improved styling
    canvas.create_rectangle(WIDTH / 2 - 200, HEIGHT / 2 - 50, WIDTH / 2 + 200, HEIGHT / 2 + 50,
                            fill='#2F4F4F', outline='white', tags="game_over")
    canvas.create_text(WIDTH / 2, HEIGHT / 2,
                       text=f"GAME OVER!\nFinal Score: {Score}\nPress R to Restart",
                       fill="white", font=("Arial", 22, "bold"), tags="game_over")


# Initialize game objects with professional styling
dino_obj = canvas.create_image(100, HEIGHT - 75, image=Dino_frames[0])
score_text = canvas.create_text(55, 45, text="Score: 0", fill='white', font=('Arial', 22, 'bold'))
pause_text = canvas.create_text(WIDTH / 2, HEIGHT / 2, text="PAUSED",
                                fill='white', font=('Arial', 36, 'bold'), state='hidden')

# Bind game controls
win.bind('<space>', jump)
win.bind('p', toggle_pause)
win.bind('P', toggle_pause)
win.bind('r', lambda event: reset_game())
win.bind('R', lambda event: reset_game())

# Start game loops
dino_animation(0)
win.after(0, update)
win.mainloop()