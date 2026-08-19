from ursina import *

app = Ursina()

# 1. Use a flattened cube for the floor. 
# A cube is always perfectly centered at 0,0,0 in Ursina.
grid_floor = Entity(
    model='cube', 
    scale=(1000, 1, 1000), 
    color=color.dark_gray, 
    texture='white_cube', 
    texture_scale=(100, 100),
    y=-10 # Lowers the floor slightly so your object sits perfectly on top
)

# 2. Place your object directly at 0, 0, 0.
plane = Entity(
    model='tailsitta.obj', 
    color=color.azure, 
    scale=2, 
    rotation=(0, 0, -90),
    position=(0, 0, 0) # Forces it to the dead center of the world
)

# Unlocks mouse controls so you can look around
EditorCamera() 

def update():
    # Moves the plane upward
    pass
    
app.run()