import turtle
import random

# --- Screen Setup ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = turtle.Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.bgcolor("#E0F7FA") # Light cyan - a soft sky color
screen.title("Cozy Cabin with Smoke")
screen.tracer(0)

# --- Turtle Pen ---
pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()
pen.penup()

# --- Helper: Draw a filled rectangle ---
def draw_filled_rectangle(t, x, y, width, height, border_color, fill_color):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.pencolor(border_color)
    t.fillcolor(fill_color)
    t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.left(90)
        t.forward(height)
        t.left(90)
    t.end_fill()
    t.penup()

# --- Draw Cabin ---
def draw_cabin(base_x, base_y):
    wall_color = "#DEB887" # BurlyWood
    roof_color = "#A0522D" # Sienna
    door_color = "#8B4513" # SaddleBrown
    window_light_color = "#FFFFE0" # LightYellow
    chimney_color = "#8B7355" # DarkKhaki (a bit like brick)

    cabin_width = 150
    cabin_height = 100
    roof_height = 60
    
    # Walls
    draw_filled_rectangle(pen, base_x, base_y, cabin_width, cabin_height, "black", wall_color)

    # Roof (triangle)
    pen.penup()
    pen.goto(base_x - 10, base_y + cabin_height) # Start slightly offset for overhang
    pen.pendown()
    pen.pencolor("black")
    pen.fillcolor(roof_color)
    pen.begin_fill()
    pen.goto(base_x + cabin_width / 2, base_y + cabin_height + roof_height)
    pen.goto(base_x + cabin_width + 10, base_y + cabin_height) # Other side overhang
    pen.goto(base_x - 10, base_y + cabin_height)
    pen.end_fill()
    pen.penup()

    # Door
    door_width = 30
    door_height = 50
    draw_filled_rectangle(pen, base_x + cabin_width / 2 - door_width / 2, base_y, door_width, door_height, "black", door_color)
    # Door knob
    pen.goto(base_x + cabin_width / 2 - door_width / 2 + 5, base_y + door_height / 2)
    pen.dot(5, "gold")


    # Window
    window_size = 25
    window_x = base_x + cabin_width * 0.7 - window_size / 2
    window_y = base_y + cabin_height * 0.5
    draw_filled_rectangle(pen, window_x, window_y, window_size, window_size, "black", window_light_color)
    # Window panes
    pen.pencolor("saddlebrown")
    pen.goto(window_x + window_size / 2, window_y)
    pen.pendown()
    pen.goto(window_x + window_size / 2, window_y + window_size)
    pen.penup()
    pen.goto(window_x, window_y + window_size / 2)
    pen.pendown()
    pen.goto(window_x + window_size, window_y + window_size / 2)
    pen.penup()
    
    # Chimney
    chimney_width = 20
    chimney_height = 35
    chimney_x = base_x + cabin_width * 0.75
    chimney_y = base_y + cabin_height + roof_height * 0.5 # Position on the roof slope
    # Adjust chimney_y based on roof slope:
    # Roof slope point: (base_x + cabin_width / 2, base_y + cabin_height + roof_height)
    # Chimney x is chimney_x. Find y on the line from (base_x + cabin_width / 2, top_roof_y) to (base_x + cabin_width + 10, base_y + cabin_height)
    # Simplified: place it visually plausible
    roof_top_y = base_y + cabin_height + roof_height
    roof_right_base_y = base_y + cabin_height
    # Assuming chimney_x is on the right slope
    percentage_along_roof_base = (chimney_x - (base_x + cabin_width / 2)) / ((cabin_width / 2) + 10)
    chimney_base_y_on_roof = roof_top_y - percentage_along_roof_base * roof_height
    
    draw_filled_rectangle(pen, chimney_x, chimney_base_y_on_roof, chimney_width, chimney_height, "black", chimney_color)
    
    return cabin_width, chimney_x + chimney_width / 2, chimney_base_y_on_roof + chimney_height # Return cabin_width and chimney top center

# --- Draw Smoke ---
def draw_smoke(start_x, start_y):
    pen.pencolor("#D3D3D3") # LightGray
    for i in range(10):
        radius = 5 + i * 0.8
        x_offset = random.randint(-5, 5) + i * 0.5 # Slight drift
        y_offset = i * 8  # Rising up
        
        pen.penup()
        pen.goto(start_x + x_offset, start_y + y_offset)
        pen.pendown()
        # Draw a partial circle to make it look like a puff
        pen.setheading(random.randint(0,360))
        for _ in range(3): # 3 arcs for a puff
            pen.circle(radius, 120) 
            pen.left(60) # Turn to make it less like a full circle
        pen.penup()

# --- Draw Tree ---
def draw_tree(base_x, base_y):
    trunk_color = "#8B4513" # SaddleBrown
    crown_color = "#228B22" # ForestGreen

    trunk_width = 20
    trunk_height = 50
    
    # Trunk
    pen.setheading(0) # Ensure upright trunk before drawing rectangle
    draw_filled_rectangle(pen, base_x - trunk_width / 2, base_y, trunk_width, trunk_height, "black", trunk_color)
    
    # Crown (multiple overlapping circles)
    crown_center_x = base_x
    crown_center_y = base_y + trunk_height + 20
    
    pen.pencolor(crown_color)
    pen.fillcolor(crown_color)
    
    for _ in range(5): # Draw a few circles for a bushy top
        offset_x = random.randint(-15, 15)
        offset_y = random.randint(-10, 10)
        radius = random.randint(20, 35)
        pen.penup()
        pen.goto(crown_center_x + offset_x, crown_center_y + offset_y - radius)
        pen.pendown()
        pen.begin_fill()
        pen.circle(radius)
        pen.end_fill()
        pen.penup()

# --- Draw Fence ---
def draw_fence(start_x, start_y, num_sections, section_width, post_height):
    pen.pencolor("#8B4513") # SaddleBrown
    pen.pensize(3)
    for i in range(num_sections + 1):
        # Draw post
        x = start_x + i * section_width
        pen.penup()
        pen.goto(x, start_y)
        pen.pendown()
        pen.goto(x, start_y + post_height)
    
    # Draw horizontal rails (2 rails)
    for j in range(2):
        rail_y = start_y + post_height * (0.3 + j * 0.4)
        pen.penup()
        pen.goto(start_x, rail_y)
        pen.pendown()
        pen.goto(start_x + num_sections * section_width, rail_y)
    pen.pensize(1) # Reset pensize
    pen.penup()

# --- Draw Ground ---
def draw_ground_plane():
    ground_color = "#90EE90" # LightGreen
    draw_filled_rectangle(pen, -SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT / 4, ground_color, ground_color)


# --- Main Drawing Logic ---
ground_level_y = -SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 4
draw_ground_plane()

# Cabin
cabin_base_x = -75
cabin_base_y = ground_level_y
cabin_width_drawn, smoke_start_x, smoke_start_y = draw_cabin(cabin_base_x, cabin_base_y)
draw_smoke(smoke_start_x, smoke_start_y)

# Trees
draw_tree(cabin_base_x - 80, ground_level_y)
# Adjust tree position relative to the drawn cabin width
draw_tree(cabin_base_x + cabin_width_drawn + 60, ground_level_y)

# Fence
draw_fence(cabin_base_x - 120, ground_level_y, 5, 30, 40) # Fence to the left
draw_fence(cabin_base_x + cabin_width_drawn + 20, ground_level_y, 4, 30, 40) # Fence to the right

# Use the returned cabin_width_drawn
draw_fence(cabin_base_x + cabin_width_drawn + 30, ground_level_y, 3, 30, 40)


# --- Finalize ---
screen.update()
screen.mainloop()