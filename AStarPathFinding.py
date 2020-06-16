#! python3
# Name: Jack Shao
# File Name: AStarPathFinding.py
# Description: a game that visualizes the A* path finding algorithm

import pygame
import math
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# FUNCTION DEFINITIONS


def onSubmit():
    # button function to retrieve text from window entries
    global start
    global end
    start_coords = startBox.get().split(',')
    end_coords = endBox.get().split(',')
    start = grid[int(start_coords[0])][int(start_coords[1])]
    end = grid[int(end_coords[0])][int(end_coords[1])]
    window.quit()
    window.destroy()


def onMousePress(mouse_position):
    # function that handles clicking of the board to turn empty squares into obstructions
    mouse_x = mouse_position[0]
    mouse_y = mouse_position[1]
    grid_x = mouse_x // (800 // columns)
    grid_y = mouse_y // (800 // rows)
    node_clicked = grid[grid_x][grid_y]
    if node_clicked != start and node_clicked != end:
        if not node_clicked.obstruction:
            node_clicked.drawNode(grey, 0)
            node_clicked.obstruction = True


def heuristic(node_1, node_2):
    distance = math.sqrt((node_1.i - node_2.i)**2 + (node_1.j - node_2.j)**2)
    return distance


def findPath():
    # the main path finding algorithm
    # it uses the the equation f = g + h (variables defined in the node class) to determine the total cost of the node
    # to see which node is the best to search
    # the algorithm ends if the end point is added to closedSet (path found) or no end is found and openSet is empty
    # (no path available)
    # it also handles the drawing of the search

    # searches every node in the open set for the best node to search
    if len(openSet) > 0:
        lowest_index = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[lowest_index].f:
                lowest_index = i

        current = openSet[lowest_index]
        # end is found
        if current == end:
            # traceback searched path and draw
            for i in range(round(current.f)):
                current.closed = False
                current.drawNode(blue, 0)
                current = current.previous

            Tk().wm_withdraw()
            result = messagebox.askokcancel('Program Finished',
                                            'The program finished, the shortest path is %s blocks away. \n Would you '
                                            'like to re-run the program?' % round(current.f))

            if result:
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                pygame.quit()

        # removes current node from openSet and add it to closedSet
        openSet.pop(lowest_index)
        closedSet.append(current)

        neighbors = current.neighbors
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            # calculates neighbors' already travelled distance and adds neighbors to openSet if neighbor node has not
            # been reached yet in previous iterations
            if neighbor not in closedSet:
                temp_g = current.g + current.value
                if neighbor in openSet:
                    if neighbor.g > temp_g:
                        neighbor.g = temp_g
                else:
                    neighbor.g = temp_g
                    openSet.append(neighbor)

            # calculates heuristic and total cost
            neighbor.h = heuristic(neighbor, end)
            neighbor.f = neighbor.g + neighbor.h

            # update previous node for later traceback if needed
            if neighbor.previous is None:
                neighbor.previous = current

    # showSearch checkbox was clicked
    if var.get():
        # color nodes in openSet and closedSet
        for i in range(len(openSet)):
            openSet[i].drawNode(red, 0)
        for i in range(len(closedSet)):
            if closedSet[i] != start and closedSet[i] != end:
                closedSet[i].drawNode(green, 0)

    current.closed = True


# CLASS DEFINITION


class node:
    # class definition of nodes on the board
    def __init__(self, x, y):
        self.i = x
        self.j = y
        self.f = 0  # total cost of the node
        self.g = 0  # distance between current node and start node
        self.h = 0  # heuristic - distance from current node to end node
        self.neighbors = []
        self.previous = None
        self.obstruction = False
        self.closed = False
        self.value = 1  # used to calculate cost of path

    def drawNode(self, color, style):
        if not self.closed:
            pygame.draw.rect(screen, color, (self.i * width, self.j * height, width, height), style)
            pygame.display.update()

    def addNeighbors(self, game_grid):
        if self.i < columns - 1 and not game_grid[self.i + 1][self.j].obstruction:
            self.neighbors.append(game_grid[self.i + 1][self.j])
        if self.i > 0 and not game_grid[self.i - 1][self.j].obstruction:
            self.neighbors.append(game_grid[self.i - 1][self.j])
        if self.j < rows - 1 and not game_grid[self.i][self.j + 1].obstruction:
            self.neighbors.append(game_grid[self.i][self.j + 1])
        if self.j > 0 and not game_grid[self.i][self.j - 1].obstruction:
            self.neighbors.append(game_grid[self.i][self.j - 1])


# initialize pygame modules
pygame.init()

# initialize used variables
screen = pygame.display.set_mode((800, 800))
columns = 50
grid = [0 for i in range(columns)]
rows = 50
openSet = []  # contains searchable nodes
closedSet = []  # contains searched nodes
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (220, 220, 220)
purple = (255, 8, 200)
black = (255, 255, 255)
width = 800 / columns
height = 800 / rows

# create 2d array
for i in range(columns):
    grid[i] = [0 for i in range(rows)]

# Create Spots
for i in range(columns):
    for j in range(rows):
        grid[i][j] = node(i, j)

# initialize start and end nodes
start = grid[1][1]
end = grid[48][48]

# draw all nodes
for i in range(columns):
    for j in range(rows):
        grid[i][j].drawNode(black, 1)

# draw borders
for i in range(rows):
    grid[0][i].drawNode(grey, 0)
    grid[0][i].obstruction = True
    grid[columns - 1][i].drawNode(grey, 0)
    grid[columns - 1][i].obstruction = True
    grid[i][0].drawNode(grey, 0)
    grid[i][0].obstruction = True
    grid[i][rows - 1].drawNode(grey, 0)
    grid[i][rows - 1].obstruction = True

# create window to set start and end locations
window = Tk()
window.title('Settings')
window.geometry('250x100')
startLabel = Label(window, text='Start(x,y): ')
startBox = Entry(window)
endLabel = Label(window, text='End(x,y): ')
endBox = Entry(window)
var = IntVar()
showSearch = ttk.Checkbutton(window, text='Show Steps', onvalue=1, offvalue=0, variable=var)
submit = Button(window, text='Submit', command=onSubmit)

startLabel.grid(row=0, pady=3)
startBox.grid(row=0, column=1, pady=3)
endLabel.grid(row=1, pady=3)
endBox.grid(row=1, column=1, pady=3)
showSearch.grid(columnspan=2, row=2)
submit.grid(columnspan=2, row=3)

window.update()
mainloop()

# start the game
start.drawNode(purple, 0)
end.drawNode(purple, 0)
openSet.append(start)

# feedback loop that allows user to draw obstructions on the board by clicking on it
# pressing the space key would break out of the loop and begin the search algorithm
loop = True
while loop:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            position = pygame.mouse.get_pos()
            onMousePress(position)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                loop = False

# add all valid reachable nodes to node data
for i in range(columns):
    for j in range(rows):
        grid[i][j].addNeighbors(grid)

# loop that calls path finding algorithmG
while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        pygame.quit()
    pygame.display.update()
    findPath()
