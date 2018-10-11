import sys
import pygame
import pygame.freetype
import time
import random
import math

class Grid:
    # Define which colors map to grid values
    colors = {
        1 : (12, 209, 209),
        2 : (239, 35, 60)
    }

    def __init__(self, display, width, height, cell_size):
        self.display = display
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid_array = [0 for i in range(self.height)]
        for n in range(len(self.grid_array)):
            self.grid_array[n] = [0 for i in range(self.width)]
    
    def get_cell(self, x, y):
        return self.grid_array[y][x]

    def set_cell(self, x, y, val):
        self.grid_array[y][x] = val

    def draw(self):
        for y in range(len(self.grid_array)):
            for x in range(len(self.grid_array[y])):
                val = self.grid_array[y][x]
                if val in Grid.colors:
                    pygame.draw.rect(self.display, Grid.colors[val], (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

class Snake:
    score = 0
    high_score = 0

    def __init__(self, grid, start_position=None):
        if start_position is None:
            start_position = (int(grid.width/2), int(grid.height/2))
        self.grid = grid
        self.points = [start_position]
        self.increase_amount = 0
        self.direction = 'right'
        self.direction_stack = []
        self.increase_length(2)
    
    def set_direction(self, direction):
        last_direction = self.direction if len(self.direction_stack) == 0 else self.direction_stack[len(self.direction_stack)-1]
        if ((direction == 'up' and last_direction != 'up' and last_direction != 'down')
                or (direction == 'down' and last_direction != 'down' and last_direction != 'up')
                or (direction == 'right' and last_direction != 'right' and last_direction != 'left')
                or (direction == 'left' and last_direction != 'left' and last_direction != 'right')):
            self.direction_stack.append(direction)

    
    def increase_length(self, amount=1):
        self.increase_amount = amount
    
    def new_apple(self):
        valid_position = False
        while not valid_position:
            x = random.randint(0, grid.width-1)
            y = random.randint(0, grid.height-1)

            valid_position = not (x, y) in self.points
            if valid_position:
                self.apple_position = (x, y)
                grid.set_cell(x, y, 2)
    
    def reset(self, start_position=None):
        # Clear all points in snake from grid
        for point in self.points:
            if (point[0] >= 0 and point[0] < self.grid.width
                    and point[1] >= 0 and point[1] < self.grid.height):
                self.grid.set_cell(point[0], point[1], 0)
        
        # Clear apple from grid
        self.grid.set_cell(self.apple_position[0], self.apple_position[1], 0)
        
        # Reset snake values
        if start_position is None:
            start_position = (int(grid.width/2), int(grid.height/2))
        self.points = [start_position]
        self.increase_amount = 0
        self.direction = 'right'
        self.direction_stack = []
        self.increase_length(2)
        Snake.score = 0

        # Add new apple
        self.new_apple()

    def update(self):
        # Update direction from the stack
        if len(self.direction_stack) > 0:
            self.direction = self.direction_stack[0]
            self.direction_stack = self.direction_stack[1:]
        
        # Move snake in direction
        first_point = self.points[len(self.points)-1]
        if self.direction == 'up':
            self.points.append((first_point[0], first_point[1]-1))
        elif self.direction == 'down':
            self.points.append((first_point[0], first_point[1]+1))
        elif self.direction == 'right':
            self.points.append((first_point[0]+1, first_point[1]))
        elif self.direction == 'left':
            self.points.append((first_point[0]-1, first_point[1]))

        # Clear end of tail (if snake is not growing)
        if self.increase_amount == 0:
            last_point = self.points[0]
            self.grid.set_cell(last_point[0], last_point[1], 0)
            self.points = self.points[1:]
        else:
            self.increase_amount -= 1

        first_point = self.points[len(self.points)-1]

        # Check for death
        if (first_point in self.points[:len(self.points)-1]
                or first_point[0] < 0 or first_point[0] > self.grid.width-1
                or first_point[1] < 0 or first_point[1] > self.grid.height-1):
            pygame.event.set_blocked(pygame.KEYDOWN)
            pygame.time.delay(2000)
            self.reset()
            pygame.event.set_allowed(pygame.KEYDOWN)
        else:
            # Check for apple
            if self.grid.get_cell(first_point[0], first_point[1]) == 2:
                self.increase_length(2)
                self.new_apple()
                Snake.score += 1
                if Snake.score > Snake.high_score:
                    Snake.high_score = Snake.score

            # Draw new head of snake
            self.grid.set_cell(first_point[0], first_point[1], 1)


BACKGROUND_COLOR = 1, 23, 47
WINDOW_SIZE = 648, 648

pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

grid = Grid(screen, 36, 36, 18)
snake = Snake(grid)
snake.new_apple()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if (event.key == 119 or event.key == 273):
                snake.set_direction('up')
            elif event.key == 115 or event.key == 274:
                snake.set_direction('down')
            elif event.key == 100 or event.key == 275:
                snake.set_direction('right')
            elif event.key == 97 or event.key == 276:
                snake.set_direction('left')

    screen.fill(BACKGROUND_COLOR)

    snake.update()
    grid.draw()

    pygame.display.flip()

    clock.tick(10)