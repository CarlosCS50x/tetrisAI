import pygame
import random
import numpy as np
from agent import Agent

# Define constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE // 2
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Define the shapes of the tetrominoes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 0],
     [0, 1, 1]],  # Z
    [[0, 1, 1],
     [1, 1, 0]],  # S
    [[1, 1, 1],
     [0, 1, 0]],  # T
    [[1, 1],
     [1, 1]],  # O
    [[1, 0, 0],
     [1, 1, 1]],  # L
    [[0, 0, 1],
     [1, 1, 1]]  # J
]

# Define the colors of the tetrominoes
COLORS = [CYAN, RED, GREEN, MAGENTA, YELLOW, ORANGE, BLUE]

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.drop_speed = 5  # Initial drop speed

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        piece = {
            'shape': shape,
            'color': color,
            'x': GRID_WIDTH // 2 - len(shape[0]) // 2,
            'y': 0
        }
        return piece

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_piece(self, piece, offset=(0, 0)):
        for y, row in enumerate(piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, piece['color'],
                                     ((piece['x'] + x + offset[0]) * BLOCK_SIZE,
                                      (piece['y'] + y + offset[1]) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))

    def draw_next_piece(self):
        next_piece_offset = (GRID_WIDTH + 1, 1)
        for y, row in enumerate(self.next_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.next_piece['color'],
                                     ((next_piece_offset[0] + x) * BLOCK_SIZE,
                                      (next_piece_offset[1] + y) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))
        next_text = self.font.render("Next:", True, WHITE)
        self.screen.blit(next_text, ((GRID_WIDTH + 1) * BLOCK_SIZE, BLOCK_SIZE))

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        for y, row in enumerate(self.grid):
            for x, cell_color in enumerate(row):
                if cell_color:
                    pygame.draw.rect(self.screen, cell_color,
                                     (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        self.draw_piece(self.current_piece)
        self.draw_next_piece()
        self.draw_score()
        pygame.display.flip()

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def check_collision(self, piece):
        for y, row in enumerate(piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    if (piece['y'] + y >= GRID_HEIGHT or
                            piece['x'] + x < 0 or piece['x'] + x >= GRID_WIDTH or
                            self.grid[piece['y'] + y][piece['x'] + x]):
                        return True
        return False

    def merge_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece['y'] + y][self.current_piece['x'] + x] = self.current_piece['color']

    def check_lines(self):
        lines_cleared = 0
        for y in range(GRID_HEIGHT):
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0] * GRID_WIDTH)
                lines_cleared += 1

        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared == 4:
            self.score += 800
        else:
            self.score += lines_cleared * 100

        # Increase speed as score increases
        self.drop_speed = max(1, 5 - self.score // 500)

    def game_over(self):
        return any(self.grid[0])

class TetrisAI(Tetris):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent

    def get_state(self):
        padded_grid = [row + [0] * (GRID_WIDTH - len(row)) for row in self.grid]
        max_length = max(len(row) for row in padded_grid)
        padded_grid = [row + [0] * (max_length - len(row)) for row in padded_grid]
        state = np.array(padded_grid, dtype=int)
        return state.ravel()


    def run(self):
        running = True
        while running:
            self.clock.tick(self.drop_speed)
            state = self.get_state()
            action = self.agent.get_action(state)
            if action == 0:  # Move left
                self.current_piece['x'] -= 1
                if self.check_collision(self.current_piece):
                    self.current_piece['x'] += 1
            elif action == 1:  # Move right
                self.current_piece['x'] += 1
                if self.check_collision(self.current_piece):
                    self.current_piece['x'] -= 1
            elif action == 2:  # Rotate
                rotated_piece = {
                    'shape': list(zip(*reversed(self.current_piece['shape']))),
                    'color': self.current_piece['color'],
                    'x': self.current_piece['x'],
                    'y': self.current_piece['y']
                }
                if not self.check_collision(rotated_piece):
                    self.current_piece['shape'] = rotated_piece['shape']
            elif action == 3:  # Drop
                while not self.check_collision(self.current_piece):
                    self.current_piece['y'] += 1
                self.current_piece['y'] -= 1

            self.current_piece['y'] += 1
            if self.check_collision(self.current_piece):
                self.current_piece['y'] -= 1
                self.merge_piece()
                self.check_lines()
                self.current_piece = self.next_piece
                self.next_piece = self.new_piece()

            self.draw()

            if self.game_over():
                running = False

        return self.score                   
