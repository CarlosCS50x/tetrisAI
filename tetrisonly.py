import pygame
import random

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
        self.dirty_rects = []

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
                    rect = pygame.Rect((piece['x'] + x + offset[0]) * BLOCK_SIZE,
                                       (piece['y'] + y + offset[1]) * BLOCK_SIZE,
                                       BLOCK_SIZE, BLOCK_SIZE)
                    self.dirty_rects.append(rect)

    def draw_next_piece(self):
        next_piece_offset = (GRID_WIDTH + 1, 1)
        for y, row in enumerate(self.next_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.next_piece['color'],
                                     ((next_piece_offset[0] + x) * BLOCK_SIZE,
                                      (next_piece_offset[1] + y) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))
                    rect = pygame.Rect((next_piece_offset[0] + x) * BLOCK_SIZE,
                                       (next_piece_offset[1] + y) * BLOCK_SIZE,
                                       BLOCK_SIZE, BLOCK_SIZE)
                    self.dirty_rects.append(rect)
        next_text = self.font.render("Next:", True, WHITE)
        self.screen.blit(next_text, ((GRID_WIDTH + 1) * BLOCK_SIZE, BLOCK_SIZE))
        rect = pygame.Rect(((GRID_WIDTH + 1) * BLOCK_SIZE, BLOCK_SIZE), next_text.get_size())
        self.dirty_rects.append(rect)

    def draw(self):
        self.screen.fill(BLACK)  # Clear the entire screen

        self.draw_grid()
        for y, row in enumerate(self.grid):
            for x, cell_color in enumerate(row):
                if cell_color:
                    pygame.draw.rect(self.screen, cell_color,
                             (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        self.draw_piece(self.current_piece)
        self.draw_next_piece()
        self.draw_score()

        # Add "Made By Zarcorp" text
        made_by_text = self.font.render("Made By Zarcorp", True, WHITE)
        made_by_rect = made_by_text.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10))
        self.screen.blit(made_by_text, made_by_rect)

        pygame.display.flip()  #

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        rect = pygame.Rect((10, 10), score_text.get_size())
        self.dirty_rects.append(rect)

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

    def handle_game_over(self):
        self.screen.fill(BLACK)
        game_over_text = self.font.render("Game Over", True, WHITE)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                          SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        restart_text = self.font.render("Press R to restart", True, WHITE)
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                                        SCREEN_HEIGHT // 2 + game_over_text.get_height()))
        pygame.display.update()

        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_restart = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting_for_restart = False
                        self.__init__()
                        return

    def run(self):
        running = True
        while running:
            self.clock.tick(self.drop_speed)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_piece['x'] -= 1
                        if self.check_collision(self.current_piece):
                            self.current_piece['x'] += 1
                    if event.key == pygame.K_RIGHT:
                        self.current_piece['x'] += 1
                        if self.check_collision(self.current_piece):
                            self.current_piece['x'] -= 1
                    if event.key == pygame.K_DOWN:
                        self.current_piece['y'] += 1
                        if self.check_collision(self.current_piece):
                            self.current_piece['y'] -= 1
                    if event.key == pygame.K_UP:
                        rotated_piece = {
                            'shape': list(zip(*reversed(self.current_piece['shape']))),
                            'color': self.current_piece['color'],
                            'x': self.current_piece['x'],
                            'y': self.current_piece['y']
                        }
                        if not self.check_collision(rotated_piece):
                            self.current_piece['shape'] = rotated_piece['shape']
                    if event.key == pygame.K_SPACE:
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
                self.handle_game_over()

        pygame.quit()

if __name__ == "__main__":
    game = Tetris()
    game.run()

