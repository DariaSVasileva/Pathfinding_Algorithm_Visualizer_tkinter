########################################################################
# Pathfinding Algorithm Visualizer program
# Using tkinter
# Python 3.8.5
# Daria Vasileva 
# 06/06/2021
########################################################################
# Sources used:
#
# @Tech With Tim: Python A* Path Finding Tutorial
# https://www.youtube.com/watch?v=JtiK0DOeI4A&ab_channel=TechWithTim
#
# @Daksh3K: Astar-Pathfinding-Algorithm-Visualization
# https://github.com/Daksh3K/Astar-Pathfinding-Algorithm-Visualization
#
# @nas-programmer: path-finding
# https://github.com/nas-programmer/path-finding
# https://www.youtube.com/watch?v=LF1h-8bEjP0&ab_channel=codeNULL
#
# @Davis MT: Python maze generator program
# https://github.com/tonypdavis/PythonMazeGenerator
# https://www.youtube.com/watch?v=Xthh4SEMA2o&ab_channel=DavisMT
#########################################################################

from tkinter import *
from tkinter import ttk
from queue import PriorityQueue
from collections import deque
import random
import time

# initialize main window
root = Tk()
root.title('Pathfinding Algorithm Visualisation')
root.maxsize(900, 900)
root.config(bg='black')

font = ("Helvetica", 11)

# Variables
selected_alg = StringVar()
selected_bld = StringVar()
WIDTH = 500
ROWS = 25
grid = []

# frame layout - for user interface
UI_frame = Frame(root, width=600, height=200, bg='black')
UI_frame.grid(row=0, column=0, padx=10, pady=5)
    
# create canvas
canvas = Canvas(root, width=WIDTH, height=WIDTH, bg='white')
canvas.grid(row=0, column=1, padx=10, pady=5) 

# define class - spot
class Spot:
    
    start_point = None
    end_point = None
    
    __slots__ = ['button','row', 'col', 'width', 'neighbors', 'g', 'h', 'f',  
                 'parent', 'start', 'end', 'barrier', 'clicked', 'total_rows']
    
    def __init__(self, row, col, width, offset, total_rows):
        
        self.button = Button(canvas,
         command = lambda a=row, b=col: self.click(a, b),
         bg='white', bd=2, relief=GROOVE
        )
        
        self.row = row
        self.col = col
        self.width = width
        
        self.button.place(x=row * width + offset, y=col * width + offset, 
                          width=width, height=width)

        self.neighbors = []
        self.g = float('inf') 
        self.h = 0
        self.f = float('inf')
        self.parent = None
        self.start = False
        self.end = False
        self.barrier = False
        self.clicked = False
        self.total_rows = total_rows
    
    def make_start(self):
        self.button.config(bg = "DarkOrange2")
        self.start = True
        self.clicked = True
        Spot.start_point = (self.col, self.row)
        
    def make_end(self):
        self.button.config(bg = "lime green")
        self.end = True
        self.clicked = True
        Spot.end_point = (self.col, self.row)
        
    def make_barrier(self):
        self.button.config(bg = "black")
        self.barrier = True
        self.clicked = True
        
    def reset(self):
        self.button.config(bg = "white")
        self.clicked = False
        
    def make_path(self):
        self.button.config(bg = "gold")
        
    def make_to_visit(self):
        self.button.config(bg = "pink")

    def make_backtracking(self):
        self.button.config(bg = "SteelBlue1")
        
    def make_open(self):
        self.button.config(bg = "cornflower blue")
        
    def make_closed(self):
        self.button.config(bg = "LightSkyBlue2")
        
    def disable(self):
        self.button.config(state=DISABLED)
    
    def enable(self):
        self.button.config(state=NORMAL)
    
    def click(self, row, col):
        if self.clicked == False:
            if not Spot.start_point:   
                self.make_start()
            elif not Spot.end_point:
                self.make_end()
            else :
                self.make_barrier()
        else:
            self.reset()
            if self.start == True:   
                self.start = False
                Spot.start_point = None
            elif self.end == True:
                self.end = False
                Spot.end_point = None
            else :
                self.barrier = False
    
    def update_neighbors(self, grid):
        self.neighbors = []

        # check neighbors a row down - if spot not outside grid and not barrier
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].barrier:
            self.neighbors.append(grid[self.row + 1][self.col]) # add spot to the neighbors

        # check neighbors a row up - if spot not outside grid and not barrier
        if self.row > 0 and not grid[self.row - 1][self.col].barrier:
            self.neighbors.append(grid[self.row - 1][self.col]) # add spot to the neighbors

        # check neighbors a col right - if spot not outside grid and not barrier
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].barrier:
            self.neighbors.append(grid[self.row][self.col + 1]) # add spot to the neighbors

        # check neighbors a col left - if spot not outside grid and not barrier
        if self.col > 0 and not grid[self.row][self.col - 1].barrier:
            self.neighbors.append(grid[self.row][self.col - 1]) # add spot to the neighbors

def make_grid(width, rows):
    gap = width // rows
    offset = 2
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, offset, rows)
            grid[i].append(spot)
    return grid

# define heuristic function - Manhatten distance
def h(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)

def reconstruct_path(spot, tickTime):
    current = spot
    while current.start == False:
        parent = current.parent
            
        parent.make_path()
        root.update_idletasks()
        time.sleep(tickTime)

        current = parent

def Reset():
    global grid
        
    Spot.start_point = None
    Spot.end_point = None
    
    for row in grid:
        for spot in row:
            spot.reset()
            spot.neighbors = []
            spot.g = float('inf') 
            spot.h = 0
            spot.f = float('inf')
            spot.parent = None
            spot.start = False
            spot.end = False
            spot.barrier = False
            spot.enable()
            
def break_wall(current, new):
    if current.row == new.row:
        if current.col > new.col:
            # wall to the left from current
            wall = grid[current.row][current.col - 1]
        else:
            # wall to the right
            wall = grid[current.row][current.col + 1]
    else:
        if current.row > new.row:
            # wall above
            wall = grid[current.row - 1][current.col]
        else:
            # wall below
            wall = grid[current.row + 1][current.col]
    # break wall
    wall.reset()
    wall.barrier = False

# A-star algorithm
def a_star(grid, tickTime):

    count = 0
    start = grid[Spot.start_point[1]][Spot.start_point[0]]
    end = grid[Spot.end_point[1]][Spot.end_point[0]]
    
    # create open_set
    open_set = PriorityQueue()
    
    # add start in open_set with f_score = 0 and count as one item
    open_set.put((0, count, start))

    # put g_score for start to 0    
    start.g = 0
    
    # calculate f_score for start using heuristic function
    start.f = h(start, end)
    
    # create a dict to keep track of spots in open_set, can't check PriorityQueue
    open_set_hash = {start}
    
    # if open_set is empty - all possible spots are considered, path doesn't exist
    while not open_set.empty():
        
        # popping the spot with lowest f_score from open_set
        # if score the same, then whatever was inserted first - PriorityQueue
        # popping [2] - spot itself
        current = open_set.get()[2]
        # syncronise with dict
        open_set_hash.remove(current)
        
        # found end?
        if current == end:
            reconstruct_path(end, tickTime)
            
            # draw end and start again
            end.make_end()
            start.make_start()
            
            # enable UI frame
            for child in UI_frame.winfo_children():
                child.configure(state='normal')
            return True
        
        # if not end - consider all neighbors of current spot to choose next step
        for neighbor in current.neighbors:
            
            # calculate g_score for every neighbor
            temp_g_score = current.g + 1
            
            # if new path through this neighbor better
            if temp_g_score < neighbor.g:
                
                # update g_score for this spot and keep track of new best path
                neighbor.parent = current
                neighbor.g = temp_g_score
                neighbor.f = temp_g_score + h(neighbor, end)
                
                if neighbor not in open_set_hash:
                    
                    # count the step
                    count += 1
                    
                    # add neighbor in open_set for consideration
                    open_set.put((neighbor.f, count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        # draw updated grid with new open_set        
        root.update_idletasks()
        time.sleep(tickTime)
        
        if current != start:
            current.make_closed()
            
    # didn't find path
    messagebox.showinfo("No Solution", "There was no solution" )

    return False

# Breadth-First algorithm
def breadth_first(grid, tickTime):
    
    start = grid[Spot.start_point[1]][Spot.start_point[0]]
    end = grid[Spot.end_point[1]][Spot.end_point[0]]
    
    open_set = deque()
    
    open_set.append(start)
    visited_hash = {start}
    
    while len(open_set) > 0:
        current = open_set.popleft()
        
        # found end?
        if current == end:
            reconstruct_path(end, tickTime)
            
            # draw end and start again
            end.make_end()
            start.make_start()
            return
        
        # if not end - consider all neighbors of current spot to choose next step
        for neighbor in current.neighbors:
            
            if neighbor not in visited_hash:
                neighbor.parent = current
                visited_hash.add(neighbor)
                open_set.append(neighbor)
                neighbor.make_open()
                
        # draw updated grid with new open_set        
        root.update_idletasks()
        time.sleep(tickTime)
        
        if current != start:
            current.make_closed()
            
    # didn't find path
    messagebox.showinfo("No Solution", "There was no solution")

    return False

# start pathfinding
def StartAlgorithm():
    global grid
    if not grid: return
    if not Spot.start_point or not Spot.end_point: 
        messagebox.showinfo("No start/end", "Place starting and ending points")
        return
    
    # update neighbors based on current maze
    for row in grid:
        for spot in row:
            spot.neighbors = []
            spot.g = float('inf') 
            spot.h = 0
            spot.f = float('inf')
            spot.parent = None
            spot.update_neighbors(grid)
            if spot.clicked == False:
                spot.reset()
            spot.disable() # disable buttons in the grid for running algorithm
    
    # disable UI frame for running algorithm
    for child in UI_frame.winfo_children():
        child.configure(state='disable')
    
    # choose algorithm
    if algMenu.get() == 'A-star Algorithm':
        a_star(grid, speedScale.get())
    elif algMenu.get() == 'Breadth-First Algorithm':
        breadth_first(grid, speedScale.get())     
        
    # enable buttons in the grid
    for row in grid:
        for spot in row:
            spot.enable()
    
    for child in UI_frame.winfo_children():
        child.configure(state='normal') # enable frame

# Put random walls in the grid
def random_walls(grid):
    
    # if start and end spots are not indicated - put start and end randomly
    if not Spot.start_point:
        current = grid[random.randint(0, ROWS - 1)][random.randint(0, ROWS - 1)]
        if current.end == False:
            current.make_start()
    
    if not Spot.end_point:
        current = grid[random.randint(0, ROWS - 1)][random.randint(0, ROWS - 1)]
        if current.start == False:
            current.make_end()
            
    start = grid[Spot.start_point[1]][Spot.start_point[0]]
    end = grid[Spot.end_point[1]][Spot.end_point[0]]
    
    # put walls randomly
    for row in grid:
        for spot in row:
            if spot != start and spot != end:
                spot.reset()
                spot.barrier = False
                spot.clicked = False
                if random.randint(0, 100) < wallsScale.get():
                    spot.make_barrier()
    
    # draw updated grid       
    root.update_idletasks()

def circ_maze(grid, rows):

    # Reset all
    Reset()

    # breake into rings
    rings = []
    for n in range(rows // 2 + 1):
        set1 = set()
        set2 = set()
        for row in grid:    
            for spot in row:
                if spot.row in range(n, rows - n) and spot.col in range(n, rows - n):
                    set1.add(spot)
                if spot.row in range(n + 1, rows - n - 1) and spot.col in range(n + 1, rows - n - 1):
                    set2.add(spot)
        ring = list(set1 - set2)
        if len(ring) > 0:
            rings.append(ring)
    
    # put start in the outer ring and end in the inner ring and remove them from rings
    random.choice(rings[0]).make_start()
    for spot in rings[0]:
        if spot.start == True:
            rings[0].remove(spot)
    
    random.choice(rings[-1]).make_end()
    for spot in rings[-1]:
        if spot.end == True:
            rings[-1].remove(spot)

    # make odd rings into walls
    for ring in rings[1::2]:
        
        # remove connor spots from rings    
        if len(ring) > 0:
            min_row = min([spot.row for spot in ring])
            max_row = max([spot.row for spot in ring])
            tmp = []
            for spot in ring:
                if (spot.row, spot.col) in [(min_row, min_row), (min_row, max_row),
                                            (max_row, min_row), (max_row, max_row)]:
                    tmp.append(spot)
            for item in tmp:
                ring.remove(item)
        
        for spot in ring:
            spot.make_barrier()
        
        if len(ring) == 0:
            rings.remove(ring)
    
    # make oppenings in ring walls
    for ring in rings[1::2]:
        for item in random.sample(ring, 2):
            item.reset()
            item.barrier = False
    
    # update neighbors based on current maze
    for row in grid:
        for spot in row:
            spot.neighbors = []
            spot.update_neighbors(grid)
    
    # add single walls between ring walls
    for ring in rings[2::2]:
        # make random spots into a wall
        tmp = []
        for spot in ring:
            if len(spot.neighbors) < 3:
                tmp.append(spot)
        if len(tmp) > 0:
            single_wall = random.choice(tmp)
            single_wall.make_barrier()        
    
    # draw updated grid       
    root.update_idletasks()
    
def carve_out(grid, rows, tickTime):

    # Reset all
    Reset()
    
    to_visit = []
    for row in grid[::2]:
        for spot in row[::2]:
            to_visit.append(spot)
        
    for row in grid:
        for spot in row:
            if spot in to_visit:
                spot.make_to_visit()
            else:
                spot.make_barrier()
    
    to_visit[0].make_start()
    to_visit[-1].make_end()
    start = grid[Spot.start_point[1]][Spot.start_point[0]]
    end = grid[Spot.end_point[1]][Spot.end_point[0]]
    
    # draw updated grid with new open_set        
    root.update_idletasks()
    time.sleep(tickTime)
    
    visited = []
    open_set = []
    current = start
    open_set.append(current)
    visited.append(current)
    
    while len(open_set) > 0:
        moves = []
        
        # right neighbor
        if current.col + 2 < rows:
            neighbor = grid[current.row][current.col + 2]
            if neighbor not in visited and neighbor in to_visit:
                moves.append(neighbor)

        # left neighbor
        if current.col - 2 >= 0:
            neighbor = grid[current.row][current.col - 2]
            if neighbor not in visited and neighbor in to_visit:
                moves.append(neighbor)
            
        # down neighbor
        if current.row + 2 < rows:
            neighbor = grid[current.row + 2][current.col]
            if neighbor not in visited and neighbor in to_visit:
                moves.append(neighbor)
            
        # up neighbor
        if current.row - 2 >= 0:
            neighbor = grid[current.row - 2][current.col]
            if neighbor not in visited and neighbor in to_visit:
                moves.append(neighbor)

        if len(moves) > 0:
            new = random.choice(moves)
            break_wall(current, new)
            if new != end:
                new.reset()
            current = new
            visited.append(current)
            open_set.append(current)
        else:
            current = open_set.pop()
            if current != start and current != end:
                current.make_backtracking()
                # draw updated grid with new open_set        
                root.update_idletasks()
                time.sleep(tickTime)
                current.reset()
            
        # draw updated grid with new open_set        
        root.update_idletasks()
        time.sleep(tickTime)
        
    # draw updated grid with new open_set        
    root.update_idletasks()
    time.sleep(tickTime)
    
# start pathfinding
def build_maze():
    global grid
    if not grid: return

    for row in grid:
        for spot in row:
            spot.disable() # disable buttons in the grid for running algorithm
    
    # disable UI frame for running algorithm
    for child in UI_frame.winfo_children():
        child.configure(state='disable')
    
    # choose algorithm
    if bldMenu.get() == 'Random walls':
        random_walls(grid)
    elif bldMenu.get() == 'Circular maze':
        circ_maze(grid, ROWS) 
    elif bldMenu.get() == 'Carved out maze':
        carve_out(grid, ROWS, speedScale.get())
        
    # enable buttons in the grid
    for row in grid:
        for spot in row:
            spot.enable()
    
    for child in UI_frame.winfo_children():
        child.configure(state='normal') # enable frame

def scale_action(event):
    if bldMenu.get() == 'Random walls':
        wallsScale.configure(state='normal')
    else:
        wallsScale.configure(state='disable')
        
def instructions():
    messagebox.showinfo("Instructions", "1. Create a maze by clicking on the grid or choose\n"
                                        "    one of the functions from the drop-down menu\n"
                                        "\n"
                                        "    You can always edit generated mazes!\n"
                                        "\n"
                                        "2. Choose one of two algorithms to find the shortest path\n"
                                        "     and visualize the search with desired speed of animation\n"
                                        "\n"
                                        "3. Reset the grid if necessary")

# User interface area
bldMenu = ttk.Combobox(UI_frame, textvariable=selected_bld, 
                       values=['Random walls', 'Circular maze', 'Carved out maze'], font = font)
bldMenu.grid(row=0, column=0, padx=5, pady=(10, 5))
bldMenu.current(0)
bldMenu.bind("<<ComboboxSelected>>", scale_action)
wallsScale = Scale(UI_frame, from_=10, to=40, resolution=5, orient=HORIZONTAL, 
                   label='Wall density', font = font, length=180)
wallsScale.grid(row=1, column=0, padx=5, pady=5, sticky=W)
Button(UI_frame, text='Build maze', command=build_maze, font = ("Helvetica", 14),
       bg='pale green').grid(row=2, column=0, padx=5, pady=(10, 20))

algMenu = ttk.Combobox(UI_frame, textvariable=selected_alg, 
                       values=['A-star Algorithm', 'Breadth-First Algorithm'], font = font)
algMenu.grid(row=3, column=0, padx=5, pady=(20, 5), sticky=W)
algMenu.current(0)
speedScale = Scale(UI_frame, from_=0.05, to=0.5, digits=2, resolution=0.05, 
                   orient=HORIZONTAL, label='Speed', font = font, length=180)
speedScale.grid(row=4, column=0, padx=5, pady=(5, 5), sticky=W)
Button(UI_frame, text='Start Search', command=StartAlgorithm, font = ("Helvetica", 14),
       bg='light salmon').grid(row=5, column=0, padx=5, pady=(10, 10))

Button(UI_frame, text='Reset', command=Reset, font = ("Helvetica", 14),
       bg='white').grid(row=6, column=0, padx=5, pady=(20, 30))

Button(UI_frame, text='Instructions', command=instructions, font = ("Helvetica", 9),
       bg='white').grid(row=7, column=0, padx=5, pady=(10, 10))

# Create grid
grid = make_grid(WIDTH, ROWS)
instructions()

# run loop 
root.mainloop()