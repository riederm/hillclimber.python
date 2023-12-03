import time
import tkinter as tk
import matplotlib.cm as cm
from numpy import stack
from PathFinder import BruteForcer, RecursivePathFinder, OrientationWalker, WalkerWithMemory1

from model import Map, Path, Walker
min_elevation = 0
max_elevation = 26
pause = 10
size = 20
steps = 5000

def elevation_to_color(elevation):
    # Normalize the elevation to a value between 0 and 1
    normalized_elevation = (elevation - min_elevation) / (max_elevation - min_elevation)
    # Use a colormap to convert the normalized elevation to a color
    color = cm.viridis(normalized_elevation)
    # Convert the color from a tuple of floats to a string in the format "#RRGGBB"
    return '#%02x%02x%02x' % (int(color[0]*255), int(color[1]*255), int(color[2]*255))

window = tk.Tk()

# read map from file
map_string = ""
with open("/workspaces/hillclimber.python/src/map.txt", "r") as f:
    map_string = f.read()
    
map = Map.from_string(map_string)
tiles = {}
#stepper = BruteForcer(map, map.start)
#stepper = WalkerWithMemory1(map, map.start)
stepper = OrientationWalker(map, map.start)


walker = Walker(map.start)

canvas = tk.Canvas(window, width=map.width*size, height=map.height*size)
canvas.pack()

rectangles = {}

is_paused = False

start = time.time_ns()

def toggle_pause():
    global is_paused
    is_paused = not is_paused
    pause_button.config(text='Continue' if is_paused else 'Pause')
    if not is_paused:
        animate_path()

pause_button = tk.Button(window, text='Pause', command=toggle_pause)
pause_button.pack()

for x in range(map.width):
    for y in range(map.height):
        field = map.get_field(x, y)
        rectangle = canvas.create_rectangle(x*size, y*size, (x+1)*size, (y+1)*size, fill=elevation_to_color(field.elevation))
        rectangles[(x, y)] = rectangle

def animate_path():
    if stepper.bestPath is not None and len(stepper.stack) == 0:
        print("done in " + str((time.time_ns() - start)/1000000) + "ms")
        toggle_pause()
    
    for x in range(steps):
        stepper.step(map, walker)
    for x in range(map.width):
        for y in range(map.height):
            rectangle = rectangles[(x, y)]
            field = map.get_field(x, y)
            if walker.path.get_length() > 0 and walker.path.get_last_step() == field:
                canvas.itemconfig(rectangle, fill='white')
            elif walker.has_walked(field):
                canvas.itemconfig(rectangle, fill='red')
            elif stepper.bestPath is not None and stepper.bestPath.field_visited(field):
                canvas.itemconfig(rectangle, fill='ghostwhite')
            else:
                canvas.itemconfig(rectangle, fill=elevation_to_color(map.get_field(x, y).elevation))

    if not is_paused:
        window.after(pause, animate_path)  # Schedule the next update in 1 second

window.after(pause, animate_path)  # Start the animation

window.mainloop()