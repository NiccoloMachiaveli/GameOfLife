import pygame
import copy

FPS = 30

# RGB Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

WIDTH = 20
HEIGHT = 20
SIZE = 8
MARGIN = 1

# Game states
MENU = 0
LEVEL_SELECT = 1
GAME = 2
INPUT = 3
RESULT = 4


class GameOfLifeEducational:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Game of Life - Binary Code Learning')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        self.state = MENU
        self.current_level = 1
        self.grid = self.create_empty_grid()
        self.target_grid = self.get_target_pattern(1)
        self.input_text = ""
        self.input_row = ""
        self.input_step = 0  # 0 - row, 1 - binary values
        self.message = ""
        self.game_running = False
        self.iterations = 0
        self.max_iterations = 10

    def create_empty_grid(self):
        grid = []
        for row in range(SIZE):
            grid.append([])
            for column in range(SIZE):
                grid[row].append(0)
        return grid

    def get_target_pattern(self, level):
        # Level 1: Square pattern (2x2) - adjusted for 8x8 grid
        if level == 1:
            target = self.create_empty_grid()
            target[3][2] = 1
            target[3][3] = 1
            target[4][2] = 1
            target[4][3] = 1
            return target
        return self.create_empty_grid()

    def defining_neighbors(self, pos, row, column):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_row = (row + i) % SIZE
                new_col = (column + j) % SIZE
                neighbors.append(pos[new_row][new_col])
        return neighbors

    def life_step(self, pos):
        new_pos = copy.deepcopy(pos)
        for row in range(SIZE):
            for column in range(SIZE):
                neighbors = self.defining_neighbors(pos, row, column)
                alive_neighbors = neighbors.count(1)

                if pos[row][column] == 1:  # Cell is alive
                    if alive_neighbors < 2 or alive_neighbors > 3:
                        new_pos[row][column] = 0
                else:  # Cell is dead
                    if alive_neighbors == 3:
                        new_pos[row][column] = 1
        return new_pos

    def draw_grid(self, grid, offset_x=50, offset_y=50):
        for row in range(SIZE):
            for column in range(SIZE):
                color = GREEN if grid[row][column] == 1 else BLACK
                pygame.draw.rect(self.screen, color,
                                 [offset_x + (MARGIN + WIDTH) * column + MARGIN,
                                  offset_y + (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH, HEIGHT])
                # Grid lines
                pygame.draw.rect(self.screen, WHITE,
                                 [offset_x + (MARGIN + WIDTH) * column + MARGIN,
                                  offset_y + (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH, HEIGHT], 1)

    def draw_menu(self):
        self.screen.fill(WHITE)

        # Title
        title = self.font.render("Game of Life - Binary Code Learning", True, BLACK)
        title_rect = title.get_rect(center=(400, 150))
        self.screen.blit(title, title_rect)

        # Menu options
        level1_text = self.font.render("Level 1", True, BLUE)
        level1_rect = level1_text.get_rect(center=(400, 250))
        self.screen.blit(level1_text, level1_rect)

        help_text = self.font.render("Help", True, BLUE)
        help_rect = help_text.get_rect(center=(400, 300))
        self.screen.blit(help_text, help_rect)

        exit_text = self.font.render("Exit", True, BLUE)
        exit_rect = exit_text.get_rect(center=(400, 350))
        self.screen.blit(exit_text, exit_rect)

        # Instructions
        instructions = [
            "Click on Level 1 to start",
            "Learn binary code through Conway's Game of Life!"
        ]

        y_offset = 450
        for instruction in instructions:
            text = self.small_font.render(instruction, True, GRAY)
            text_rect = text.get_rect(center=(400, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 30

        return level1_rect, help_rect, exit_rect

    def draw_input_screen(self):
        self.screen.fill(WHITE)

        # Title
        title = self.font.render(f"Level {self.current_level} - Input Setup", True, BLACK)
        title_rect = title.get_rect(center=(400, 50))
        self.screen.blit(title, title_rect)

        # Target pattern
        target_title = self.font.render("Target Pattern:", True, BLACK)
        self.screen.blit(target_title, (50, 100))
        self.draw_grid(self.target_grid, 50, 130)

        # Current grid
        current_title = self.font.render("Your Setup:", True, BLACK)
        self.screen.blit(current_title, (400, 100))
        self.draw_grid(self.grid, 400, 130)

        # Input instructions and current step display
        if self.input_step == 0:
            instruction = f"Enter row number (0-{SIZE - 1}):"
            input_display = self.input_text
            step_info = "Step 1: Choose row"
        else:
            instruction = f"Enter character for row {self.input_row}:"
            input_display = self.input_text
            step_info = f"Step 2: Character for row {self.input_row}"

        # Step indicator
        step_text = self.small_font.render(step_info, True, BLUE)
        self.screen.blit(step_text, (50, 370))

        instr_text = self.small_font.render(instruction, True, BLACK)
        self.screen.blit(instr_text, (50, 400))

        # Input box with better visibility
        input_box = pygame.Rect(50, 430, 300, 35)
        pygame.draw.rect(self.screen, WHITE, input_box)
        pygame.draw.rect(self.screen, BLUE, input_box, 2)

        # Show input with cursor
        display_text = input_display + "|" if len(input_display) < (2 if self.input_step == 0 else 1) else input_display
        input_surface = self.font.render(display_text, True, BLACK)
        self.screen.blit(input_surface, (input_box.x + 10, input_box.y + 5))

        # Buttons
        start_button = pygame.Rect(50, 520, 100, 40)
        pygame.draw.rect(self.screen, GREEN, start_button)
        start_text = self.font.render("Start", True, BLACK)
        start_rect = start_text.get_rect(center=start_button.center)
        self.screen.blit(start_text, start_rect)

        reset_button = pygame.Rect(170, 520, 100, 40)
        pygame.draw.rect(self.screen, RED, reset_button)
        reset_text = self.font.render("Reset", True, BLACK)
        reset_rect = reset_text.get_rect(center=reset_button.center)
        self.screen.blit(reset_text, reset_rect)

        # Message with better positioning
        if self.message:
            msg_text = self.small_font.render(self.message, True,
                                              RED if "must" in self.message or "Invalid" in self.message else GREEN)
            self.screen.blit(msg_text, (50, 475))

        # Example text
        if self.input_step == 1:
            example = "Example: 'H' -> 01001000, '0' -> 00110000"
            example_text = self.small_font.render(example, True, GRAY)
            self.screen.blit(example_text, (50, 495))

        return start_button, reset_button

    def draw_game_screen(self):
        self.screen.fill(WHITE)

        # Title
        title = self.font.render(f"Level {self.current_level} - Iteration {self.iterations}", True, BLACK)
        title_rect = title.get_rect(center=(400, 30))
        self.screen.blit(title, title_rect)

        # Target vs Current
        target_title = self.small_font.render("Target:", True, BLACK)
        self.screen.blit(target_title, (100, 80))
        self.draw_grid(self.target_grid, 50, 100)

        current_title = self.small_font.render("Current:", True, BLACK)
        self.screen.blit(current_title, (450, 80))
        self.draw_grid(self.grid, 400, 100)

        # Controls
        controls = [
            "Press SPACE to step forward",
            "Press R to restart level",
            "Press ESC to return to menu"
        ]

        y_offset = 450
        for control in controls:
            text = self.small_font.render(control, True, GRAY)
            self.screen.blit(text, (50, y_offset))
            y_offset += 25

    def draw_result_screen(self, success):
        self.screen.fill(WHITE)

        if success:
            title = self.font.render("Congratulations! Level Complete!", True, GREEN)
            message = "You successfully created the target pattern!"
        else:
            title = self.font.render("Level Failed", True, RED)
            message = "The pattern didn't match. Try again!"

        title_rect = title.get_rect(center=(400, 200))
        self.screen.blit(title, title_rect)

        msg_text = self.small_font.render(message, True, BLACK)
        msg_rect = msg_text.get_rect(center=(400, 250))
        self.screen.blit(msg_text, msg_rect)

        # Buttons
        retry_button = pygame.Rect(250, 350, 100, 40)
        pygame.draw.rect(self.screen, BLUE, retry_button)
        retry_text = self.font.render("Retry", True, WHITE)
        retry_rect = retry_text.get_rect(center=retry_button.center)
        self.screen.blit(retry_text, retry_rect)

        menu_button = pygame.Rect(370, 350, 100, 40)
        pygame.draw.rect(self.screen, GRAY, menu_button)
        menu_text = self.font.render("Menu", True, WHITE)
        menu_rect = menu_text.get_rect(center=menu_button.center)
        self.screen.blit(menu_text, menu_rect)

        return retry_button, menu_button

    def process_symbol_input(self, row, symbol):
        try:
            row_num = int(row)
            if row_num < 0 or row_num >= SIZE:
                return False, f"Row number must be between 0 and {SIZE - 1}"

            if len(symbol) != 1:
                return False, "Please enter exactly one character"

            # Convert symbol to 8-bit binary
            ascii_value = ord(symbol)
            binary_str = format(ascii_value, '08b')  # 8-bit binary

            # Apply binary to grid row
            for i in range(SIZE):
                self.grid[row_num][i] = int(binary_str[i])

            return True, f"'{symbol}' (ASCII {ascii_value}) -> {binary_str} applied to row {row_num}"
        except ValueError:
            return False, "Invalid row number"
        except Exception as e:
            return False, f"Error processing symbol: {str(e)}"

    def grids_match(self, grid1, grid2):
        for row in range(SIZE):
            for col in range(SIZE):
                if grid1[row][col] != grid2[row][col]:
                    return False
        return True

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == MENU:
                        level1_rect, help_rect, exit_rect = self.draw_menu()
                        if level1_rect.collidepoint(event.pos):
                            self.state = INPUT
                            self.current_level = 1
                            self.grid = self.create_empty_grid()
                            self.target_grid = self.get_target_pattern(1)
                        elif exit_rect.collidepoint(event.pos):
                            running = False

                    elif self.state == INPUT:
                        start_button, reset_button = self.draw_input_screen()
                        if start_button.collidepoint(event.pos):
                            self.state = GAME
                            self.game_running = True
                            self.iterations = 0
                        elif reset_button.collidepoint(event.pos):
                            self.grid = self.create_empty_grid()
                            self.input_text = ""
                            self.input_row = ""
                            self.input_step = 0
                            self.message = ""

                    elif self.state == RESULT:
                        retry_button, menu_button = self.draw_result_screen(False)
                        if retry_button.collidepoint(event.pos):
                            self.state = INPUT
                            self.grid = self.create_empty_grid()
                            self.input_text = ""
                            self.input_row = ""
                            self.input_step = 0
                            self.message = ""
                        elif menu_button.collidepoint(event.pos):
                            self.state = MENU

                elif event.type == pygame.KEYDOWN:
                    if self.state == INPUT:
                        if event.key == pygame.K_RETURN:
                            if self.input_step == 0:  # Row input
                                if self.input_text.isdigit():
                                    row_num = int(self.input_text)
                                    if 0 <= row_num < SIZE:
                                        self.input_row = self.input_text
                                        self.input_text = ""
                                        self.input_step = 1
                                        self.message = f"Now enter 8-bit binary for row {row_num}"
                                    else:
                                        self.message = f"Row must be between 0 and {SIZE - 1}"
                                else:
                                    self.message = "Please enter a valid number"
                            else:  # Binary input
                                success, msg = self.process_symbol_input(self.input_row, self.input_text)
                                self.message = msg
                                if success:
                                    self.input_text = ""
                                    self.input_row = ""
                                    self.input_step = 0
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        elif event.key == pygame.K_ESCAPE:
                            self.state = MENU
                        else:
                            # Filter input based on current step
                            if self.input_step == 0:  # Row input - only digits
                                if event.unicode.isdigit() and len(self.input_text) < 1:
                                    self.input_text += event.unicode
                            else:  # Symbol input - any printable character
                                if len(self.input_text) < 1 and event.unicode.isprintable():
                                    self.input_text += event.unicode

                    elif self.state == GAME:
                        if event.key == pygame.K_SPACE:
                            if self.iterations < self.max_iterations:
                                self.grid = self.life_step(self.grid)
                                self.iterations += 1

                                if self.grids_match(self.grid, self.target_grid):
                                    self.state = RESULT
                                elif self.iterations >= self.max_iterations:
                                    self.state = RESULT
                        elif event.key == pygame.K_r:
                            self.state = INPUT
                            self.grid = self.create_empty_grid()
                        elif event.key == pygame.K_ESCAPE:
                            self.state = MENU

            # Draw current state
            if self.state == MENU:
                self.draw_menu()
            elif self.state == INPUT:
                self.draw_input_screen()
            elif self.state == GAME:
                self.draw_game_screen()
            elif self.state == RESULT:
                success = self.grids_match(self.grid, self.target_grid)
                self.draw_result_screen(success)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    game = GameOfLifeEducational()
    game.run()