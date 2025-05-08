import turtle
import random
import colorsys # For color manipulation if needed

# --- Screen Setup ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = turtle.Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.bgcolor("#E0F7FA") # Light cyan - a soft sky color
screen.title("Cozy Cabin with Animated Smoke")
screen.tracer(0)

# --- Turtle Pens ---
pen = turtle.Turtle() # For static elements
pen.speed(0)
pen.hideturtle()
pen.penup()

smoke_pen = turtle.Turtle() # For dynamic smoke
smoke_pen.speed(0)
smoke_pen.hideturtle()
smoke_pen.penup()

sun_effects_pen = turtle.Turtle() # For sun rays
sun_effects_pen.speed(0)
sun_effects_pen.hideturtle()
sun_effects_pen.penup()

# --- Global Smoke Particle List ---
smoke_particles = []
SMOKE_START_X = 0 # Will be updated after cabin is drawn
SMOKE_START_Y = 0
SMOKE_CREATION_INTERVAL = 5 # Create smoke every N frames
smoke_frame_count = 0

# --- Global Window Light Details ---
cabin_window_details = {
    'x': 0, 'y': 0, 'size': 0,
    'colors': ["#FFFFE0", "#FFEEB0"], # LightYellow, Slightly dimmer/warmer yellow
    'current_color_index': 0,
    'border_color': "black",
    'pane_color': "saddlebrown"
}
WINDOW_FLICKER_INTERVAL = 15 # Flicker every N frames (e.g., 15 frames = 0.75 seconds at 20FPS)
window_frame_count = 0

# --- Global Sun Details for Animation ---
sun_details = {
    'x': 0, 'y': 0, 'radius': 0, 'color': "gold", # Will be populated
    'ray_color': "#FFFFA0", # Light yellow for rays
    'num_rays': 12,
    'ray_length_short': 7,
    'ray_length_long': 12,
    'current_ray_length': 12
}
SUN_RAY_FLICKER_INTERVAL = 8 # Flicker rays every N frames
sun_ray_frame_count = 0


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

# --- Draw Sun ---
def draw_sun(t, x, y, radius, color):
    original_heading = t.heading()
    original_pencolor = t.pencolor()
    original_fillcolor = t.fillcolor()
    t.penup()
    t.goto(x, y - radius)
    t.pendown()
    t.pencolor(color)
    t.fillcolor(color)
    t.begin_fill()
    t.circle(radius)
    t.end_fill()
    t.pencolor(original_pencolor)
    t.fillcolor(original_fillcolor)
    t.setheading(original_heading)
    t.penup()

# --- Draw Cabin ---
def draw_cabin(base_x, base_y):
    wall_color = "#DEB887"
    roof_color = "#A0522D"
    door_color = "#8B4513"
    window_light_color = "#FFFFE0"
    chimney_color = "#8B7355"
    cabin_width = 150
    cabin_height = 100
    roof_height = 60
    draw_filled_rectangle(pen, base_x, base_y, cabin_width, cabin_height, "black", wall_color)
    pen.penup()
    pen.goto(base_x - 10, base_y + cabin_height)
    pen.pendown()
    pen.pencolor("black")
    pen.fillcolor(roof_color)
    pen.begin_fill()
    pen.goto(base_x + cabin_width / 2, base_y + cabin_height + roof_height)
    pen.goto(base_x + cabin_width + 10, base_y + cabin_height)
    pen.goto(base_x - 10, base_y + cabin_height)
    pen.end_fill()
    pen.penup()
    door_width = 30
    door_height = 50
    draw_filled_rectangle(pen, base_x + cabin_width / 2 - door_width / 2, base_y, door_width, door_height, "black", door_color)
    pen.goto(base_x + cabin_width / 2 - door_width / 2 + 5, base_y + door_height / 2)
    pen.dot(5, "gold")
    window_size = 25
    window_x = base_x + cabin_width * 0.7 - window_size / 2
    window_y = base_y + cabin_height * 0.5
    
    # Store window details for animation
    global cabin_window_details # Ensure we are modifying the global dict
    cabin_window_details['x'] = window_x
    cabin_window_details['y'] = window_y
    cabin_window_details['size'] = window_size
    # cabin_window_details['border_color'] and ['pane_color'] are already set globally
    # cabin_window_details['colors'] and ['current_color_index'] are also set globally

    # Initial draw of the window using details from the global dict
    initial_light_color = cabin_window_details['colors'][cabin_window_details['current_color_index']]
    draw_filled_rectangle(pen, window_x, window_y, window_size, window_size, cabin_window_details['border_color'], initial_light_color)
    
    # Window panes
    pen.pencolor(cabin_window_details['pane_color'])
    pen.goto(window_x + window_size / 2, window_y)
    pen.pendown()
    pen.goto(window_x + window_size / 2, window_y + window_size)
    pen.penup()
    pen.goto(window_x, window_y + window_size / 2)
    pen.pendown()
    pen.goto(window_x + window_size, window_y + window_size / 2)
    pen.penup()
    chimney_width = 20
    chimney_height = 35
    chimney_x_local = cabin_width * 0.75 # Relative to cabin base_x
    # Simplified chimney y placement
    chimney_on_roof_y_offset = cabin_height + roof_height * 0.6 
    draw_filled_rectangle(pen, base_x + chimney_x_local, base_y + chimney_on_roof_y_offset - chimney_height*0.3, chimney_width, chimney_height, "black", chimney_color)
    return cabin_width, base_x + chimney_x_local + chimney_width / 2, base_y + chimney_on_roof_y_offset + chimney_height*0.7

# --- Smoke Particle System ---
def create_smoke_particle(start_x, start_y):
    particle = {
        'x': start_x + random.uniform(-2, 2),
        'y': start_y + random.uniform(-2, 2),
        'dx': random.uniform(-0.3, 0.3), # Horizontal drift
        'dy': random.uniform(0.5, 1.2),  # Vertical speed
        'radius': random.uniform(3, 6),
        'max_life': random.randint(80, 150), # Frames to live
        'life': 0, # Current age
        'initial_alpha': 0.7 # For color
    }
    particle['life'] = particle['max_life'] # Start with full life
    smoke_particles.append(particle)

def update_and_draw_all_smoke():
    global smoke_particles
    smoke_pen.clear() # Clear previous frame's smoke
    
    new_particles = []
    for p in smoke_particles:
        p['x'] += p['dx']
        p['y'] += p['dy']
        p['life'] -= 1
        
        if p['life'] > 0:
            new_particles.append(p)
            # Calculate alpha (0.0 to 1.0)
            alpha = (p['life'] / p['max_life']) * p['initial_alpha']
            alpha = max(0, min(1, alpha)) # Clamp between 0 and 1
            
            # Convert alpha to a grayscale color (e.g., (r,g,b) where r=g=b)
            # Turtle colors are usually strings or (r,g,b) tuples from 0-1 or 0-255
            # For simplicity, let's use a dot with varying size and a fixed light gray
            # A more advanced way is to change color from gray to background color
            
            # Simple: size decreases, color fixed
            current_radius = p['radius'] * (p['life'] / p['max_life'])
            if current_radius > 0.5: # Only draw if reasonably visible
                smoke_pen.penup()
                smoke_pen.goto(p['x'], p['y'])
                # smoke_pen.dot(current_radius * 2, "#E0E0E0") # Light gray dot
                
                # Draw puff using circles (like original static smoke)
                smoke_pen.pencolor(f"#{int(200 + alpha*50):02x}{int(200 + alpha*50):02x}{int(200 + alpha*50):02x}") # Fading gray
                smoke_pen.pendown()
                original_heading = smoke_pen.heading()
                smoke_pen.setheading(random.randint(0,360))
                for _ in range(3):
                     smoke_pen.circle(current_radius, 100 + alpha * 20)
                     smoke_pen.left(50 + alpha * 10)
                smoke_pen.setheading(original_heading)
                smoke_pen.penup()

    smoke_particles = new_particles


# --- Draw Tree ---
def draw_tree(base_x, base_y):
    trunk_color = "#8B4513"
    crown_color = "#228B22"
    trunk_width = 20
    trunk_height = 50
    pen.setheading(0)
    draw_filled_rectangle(pen, base_x - trunk_width / 2, base_y, trunk_width, trunk_height, "black", trunk_color)
    crown_center_x = base_x
    crown_center_y = base_y + trunk_height + 20
    original_pencolor = pen.pencolor()
    original_fillcolor = pen.fillcolor()
    pen.pencolor(crown_color)
    pen.fillcolor(crown_color)
    for _ in range(5):
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
    pen.pencolor(original_pencolor)
    pen.fillcolor(original_fillcolor)


# --- Draw Fence ---
def draw_fence(start_x, start_y, num_sections, section_width, post_height):
    original_pencolor = pen.pencolor()
    original_pensize = pen.pensize()
    pen.pencolor("#8B4513")
    pen.pensize(3)
    for i in range(num_sections + 1):
        x = start_x + i * section_width
        pen.penup()
        pen.goto(x, start_y)
        pen.pendown()
        pen.goto(x, start_y + post_height)
    for j in range(2):
        rail_y = start_y + post_height * (0.3 + j * 0.4)
        pen.penup()
        pen.goto(start_x, rail_y)
        pen.pendown()
        pen.goto(start_x + num_sections * section_width, rail_y)
    pen.pensize(original_pensize)
    pen.pencolor(original_pencolor)
    pen.penup()

# --- Draw Holding Hands Couple Silhouette ---
def draw_holding_hands_couple_silhouette(t, base_x, base_y, scale=1.0, color="black"):
    t.penup()
    t.pencolor(color)
    t.pensize(2 * scale) # Make lines a bit thicker based on scale

    # Dimensions for stick figures
    head_radius = 8 * scale
    body_height = 30 * scale
    arm_length = 15 * scale
    leg_length = 20 * scale
    person_spacing = 22 * scale # Increased space between people to prevent head overlap (was 15)

    # --- Helper to draw one stick person ---
    def draw_stick_person(person_center_x, person_base_y, is_left_person):
        # Head
        t.penup()
        t.goto(person_center_x, person_base_y + body_height + head_radius) # Center of head
        t.pendown()
        t.circle(head_radius)

        # Body
        neck_y = person_base_y + body_height
        t.penup()
        t.goto(person_center_x, neck_y)
        t.pendown()
        t.goto(person_center_x, person_base_y) # Body line down to base

        # Legs
        leg_angle = 30 # Angle from vertical
        # Left leg
        t.penup()
        t.goto(person_center_x, person_base_y)
        t.pendown()
        t.setheading(270 - leg_angle) # Down-left
        t.forward(leg_length)
        # Right leg
        t.penup()
        t.goto(person_center_x, person_base_y)
        t.pendown()
        t.setheading(270 + leg_angle) # Down-right
        t.forward(leg_length)

        # Arms
        shoulder_y = person_base_y + body_height * 0.75
        # Outer arm
        t.penup()
        t.goto(person_center_x, shoulder_y)
        t.pendown()
        if is_left_person:
            t.setheading(180 + 45) # Out and down-left
        else:
            t.setheading(0 - 45)   # Out and down-right
        t.forward(arm_length * 0.8) # Outer arm slightly shorter

        # Inner arm (for holding hands)
        t.penup()
        t.goto(person_center_x, shoulder_y)
        t.pendown()
        if is_left_person:
            t.setheading(0) # Straight right
        else:
            t.setheading(180) # Straight left
        t.forward(arm_length / 2) # Arm reaches halfway to the center
        return t.pos() # Return hand position

    # --- Draw the two people ---
    p1_center_x = base_x - person_spacing / 2
    p2_center_x = base_x + person_spacing / 2

    hand_pos1 = draw_stick_person(p1_center_x, base_y, True)
    hand_pos2 = draw_stick_person(p2_center_x, base_y, False)

    # Connect hands (optional, if they don't meet perfectly)
    # For stick figures, just having arms point to each other is often enough
    # If a direct line is desired:
    # t.penup()
    # t.goto(hand_pos1)
    # t.pendown()
    # t.goto(hand_pos2)
    
    t.penup()
    t.pensize(1) # Reset pensize
# --- Draw Ground ---
def draw_ground_plane():
    ground_color = "#90EE90"
    draw_filled_rectangle(pen, -SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT / 4, ground_color, ground_color)

# --- Animation Loop ---
def animate_scene():
    global smoke_frame_count, SMOKE_START_X, SMOKE_START_Y
    global window_frame_count, cabin_window_details
    global sun_ray_frame_count, sun_details, sun_effects_pen
    
    # Animate Smoke
    smoke_frame_count +=1
    if smoke_frame_count % SMOKE_CREATION_INTERVAL == 0:
        create_smoke_particle(SMOKE_START_X, SMOKE_START_Y)
        if len(smoke_particles) > 60 : # Limit max particles slightly more
             smoke_particles.pop(0)
    update_and_draw_all_smoke()

    # Animate Window Light
    window_frame_count += 1
    if window_frame_count % WINDOW_FLICKER_INTERVAL == 0:
        cabin_window_details['current_color_index'] = 1 - cabin_window_details['current_color_index'] # Toggle 0 and 1
        new_light_color = cabin_window_details['colors'][cabin_window_details['current_color_index']]
        
        w_x = cabin_window_details['x']
        w_y = cabin_window_details['y']
        w_size = cabin_window_details['size']
        
        # Redraw window light fill
        # Important: Use the main 'pen' for this as it's part of the static scene structure
        original_pen_pencolor = pen.pencolor()
        original_pen_fillcolor = pen.fillcolor()
        
        pen.pencolor(new_light_color) # Match border to fill to avoid issues when filling over
        pen.fillcolor(new_light_color)
        pen.penup()
        pen.goto(w_x, w_y)
        pen.pendown()
        pen.begin_fill()
        for _ in range(2): # Draw rectangle path
            pen.forward(w_size)
            pen.left(90)
            pen.forward(w_size)
            pen.left(90)
        pen.end_fill()
        pen.penup()
        
        # Redraw window panes over the new fill
        pen.pencolor(cabin_window_details['pane_color'])
        pen.penup()
        pen.goto(w_x + w_size / 2, w_y)
        pen.pendown()
        pen.goto(w_x + w_size / 2, w_y + w_size) # Vertical pane
        pen.penup()
        pen.goto(w_x, w_y + w_size / 2)
        pen.pendown()
        pen.goto(w_x + w_size, w_y + w_size / 2) # Horizontal pane
        pen.penup()

        pen.pencolor(original_pen_pencolor) # Restore pen's original colors
        pen.fillcolor(original_pen_fillcolor)

    # Animate Sun Rays
    sun_effects_pen.clear() # Clear previous rays
    sun_ray_frame_count += 1
    if sun_ray_frame_count % SUN_RAY_FLICKER_INTERVAL == 0:
        if sun_details['current_ray_length'] == sun_details['ray_length_long']:
            sun_details['current_ray_length'] = sun_details['ray_length_short']
        else:
            sun_details['current_ray_length'] = sun_details['ray_length_long']

    if sun_details['radius'] > 0: # Only draw if sun is initialized
        num_rays = sun_details['num_rays']
        actual_ray_length = sun_details['current_ray_length']
        sun_center_x = sun_details['x']
        sun_center_y = sun_details['y']
        
        sun_effects_pen.pencolor(sun_details['ray_color'])
        sun_effects_pen.pensize(2)
        for i in range(num_rays):
            angle = (360 / num_rays) * i + (sun_ray_frame_count % (360 // num_rays)) # Slight rotation effect
            sun_effects_pen.penup()
            sun_effects_pen.goto(sun_center_x, sun_center_y)
            sun_effects_pen.setheading(angle)
            sun_effects_pen.forward(sun_details['radius'] * 0.8) # Start rays slightly inside the sun for better look
            sun_effects_pen.pendown()
            sun_effects_pen.forward(actual_ray_length)
        sun_effects_pen.penup()

    screen.update()
    screen.ontimer(animate_scene, 50) # Approx 20 FPS

# --- Main Drawing Logic ---
sun_radius = 40
sun_padding = 30
sun_x_pos = -SCREEN_WIDTH / 2 + sun_radius + sun_padding
sun_y_pos = SCREEN_HEIGHT / 2 - sun_radius - sun_padding
draw_sun(pen, sun_x_pos, sun_y_pos, sun_radius, "gold")
# Populate sun_details (note: sun_y_pos is the top-left reference for draw_sun, actual center is y_pos)
sun_details['x'] = sun_x_pos
sun_details['y'] = sun_y_pos
sun_details['radius'] = sun_radius
sun_details['color'] = "gold"


ground_level_y = -SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 4
draw_ground_plane()

cabin_base_x = -75
cabin_base_y = ground_level_y
cabin_width_drawn, SMOKE_START_X, SMOKE_START_Y = draw_cabin(cabin_base_x, cabin_base_y)
# Static smoke call removed

draw_tree(cabin_base_x - 80, ground_level_y)
draw_tree(cabin_base_x + cabin_width_drawn + 60, ground_level_y)

draw_fence(cabin_base_x - 120, ground_level_y, 5, 30, 40)
draw_fence(cabin_base_x + cabin_width_drawn + 20, ground_level_y, 4, 30, 40)

last_fence_start_x = cabin_base_x + cabin_width_drawn + 30
last_fence_sections = 3
last_fence_section_width = 30
draw_fence(last_fence_start_x, ground_level_y, last_fence_sections, last_fence_section_width, 40)

# Draw holding hands couple silhouette
# Position after the last fence on the right + some spacing
couple_base_x = last_fence_start_x + (last_fence_sections * last_fence_section_width) + 70
draw_holding_hands_couple_silhouette(pen, couple_base_x, ground_level_y, scale=0.8)

screen.update() # Initial draw of static elements
animate_scene() # Start animation

screen.mainloop()