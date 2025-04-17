import math,random, pygame

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""

class SudokuGenerator:
    '''
    create a sudoku board - initialize class variables and set up the 2D board
    This should initialize:
    self.row_length		- the length of each row
    self.removed_cells	- the total number of cells to be removed
    self.board			- a 2D list of ints to represent the board
    self.box_length		- the square root of row_length

    Parameters:
    row_length is the number of rows/columns of the board (always 9 for this project)
    removed_cells is an integer value - the number of cells to be removed

    Return:
    None
    '''
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.box_length = int(math.sqrt(self.row_length))
        self.board = []

        for i in range(self.row_length):
            row = []
            for j in range(self.row_length):
                row.append(0)
            self.board.append(row)

    '''
	Returns a 2D python list of numbers which represents the board

	Parameters: None
	Return: list[list]
    '''
    def get_board(self):
        return self.board

    '''
	Displays the board to the console
    This is not strictly required, but it may be useful for debugging purposes

	Parameters: None
	Return: None
    '''
    def print_board(self):
        for row in self.board:
            line = ""
            for num in row:
                if num != 0:
                    line += str(num) + " "
                else:
                    line += ". "
            print(line)

    '''
	Determines if num is contained in the specified row (horizontal) of the board
    If num is already in the specified row, return False. Otherwise, return True

	Parameters:
	row is the index of the row we are checking
	num is the value we are looking for in the row
	
	Return: boolean
    '''
    def valid_in_row(self, row, num):
        for col in range(self.row_length):
            if self.board[row][col] == num:
                return False
        return True

    '''
	Determines if num is contained in the specified column (vertical) of the board
    If num is already in the specified col, return False. Otherwise, return True

	Parameters:
	col is the index of the column we are checking
	num is the value we are looking for in the column
	
	Return: boolean
    '''
    def valid_in_col(self, col, num):
        for row in range(self.row_length):
            if self.board[row][col] == num:
                return False
        return True

    '''
	Determines if num is contained in the 3x3 box specified on the board
    If num is in the specified box starting at (row_start, col_start), return False.
    Otherwise, return True

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
	num is the value we are looking for in the box

	Return: boolean
    '''
    def valid_in_box(self, row_start, col_start, num):
        for r in range(row_start, row_start + 3):
            for c in range(col_start, col_start + 3):
                if self.board[r][c] == num:
                    return False
        return True
    
    '''
    Determines if it is valid to enter num at (row, col) in the board
    This is done by checking that num is unused in the appropriate, row, column, and box

	Parameters:
	row and col are the row index and col index of the cell to check in the board
	num is the value to test if it is safe to enter in this cell

	Return: boolean
    '''
    def is_valid(self, row, col, num):
        row_valid = self.valid_in_row(row, num)
        col_valid = self.valid_in_col(col, num)
        box_valid = self.valid_in_box(row - row % 3, col - col % 3, num)
        return row_valid and col_valid and box_valid

    '''
    Fills the specified 3x3 box with values
    For each position, generates a random digit which has not yet been used in the box

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)

	Return: None
    '''
    def fill_box(self, row_start, col_start):
        nums = []
        for i in range(1, 10):
            nums.append(i)

        random.shuffle(nums)

        index = 0
        for r in range(3):
            for c in range(3):
                self.board[row_start + r][col_start + c] = nums[index]
                index += 1
    
    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)

	Parameters: None
	Return: None
    '''
    def fill_diagonal(self):
        for i in range(0, self.row_length, self.box_length):
            self.fill_box(i, i)

    '''
    DO NOT CHANGE
    Provided for students
    Fills the remaining cells of the board
    Should be called after the diagonal boxes have been filled
	
	Parameters:
	row, col specify the coordinates of the first empty (0) cell

	Return:
	boolean (whether or not we could solve the board)
    '''
    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True
        
        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
    DO NOT CHANGE
    Provided for students
    Constructs a solution by calling fill_diagonal and fill_remaining

	Parameters: None
	Return: None
    '''
    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    '''
    Removes the appropriate number of cells from the board
    This is done by setting some values to 0
    Should be called after the entire solution has been constructed
    i.e. after fill_values has been called
    
    NOTE: Be careful not to 'remove' the same cell multiple times
    i.e. if a cell is already 0, it cannot be removed again

	Parameters: None
	Return: None
    '''
    def remove_cells(self):
        count = 0
        while count < self.removed_cells:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                count += 1

'''
DO NOT CHANGE
Provided for students
Given a number of rows and number of cells to remove, this function:
1. creates a SudokuGenerator
2. fills its values and saves this as the solved state
3. removes the appropriate number of cells
4. returns the representative 2D Python Lists of the board and solution

Parameters:
size is the number of rows/columns of the board (9 for this project)
removed is the number of cells to clear (set to 0)

Return: list[list] (a 2D Python list to represent the board)
'''
def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board

#Cell Class

class Cell:

    #Cell class iniz
    #getting the value of the cell, the position, and which screen should be displayed
    #also whether or not the cell is selected to be changed
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False

    #setting a cells value
    def set_cell_value(self,value):
        self.value = value

    #Temp value of a cell
    def set_sketched_value(self,value):
        self.tempValue = value

    #drawing the cell
    def draw(self):

        #size of cell
        cell_width = 540 // 9
        cell_height = 540 // 9
        x = self.col * cell_width
        y = self.row * cell_height

        #Font of game
        font = pygame.font.SysFont("arial", 30)

        #value of cell. Actual or sketched
        if self.value != 0:
            text = font.render(self.value, True, (255, 255, 255))
            text_rect = text.get_rect(center = (x + cell_width // 2, y + cell_height // 2))
            self.screen.blit(text, text_rect)
        elif self.tempValue != 0:
            sketchFont = pygame.font.SysFont("arial", 15)
            sketchText = sketchFont.render(self.tempValue, True, (255, 255, 255))
            self.screen.blit(sketchText, (x + cell_width // 2, y + cell_height // 2))


        #selected cell drawing
        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, cell_width, cell_height), 3)
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), (x, y, cell_width, cell_height), 1)


def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((540, 540))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    mousex, mousey = event.pos
    finally:
        pygame.quit()

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.selected_cell = None
        self.board_values = generate_sudoku(9, difficulty)
        self.original_board = [row[:] for row in self.board_values]
        self.cells = [[Cell(self.board_values[row][col], row, col, screen) for col in range(9)] for row in range(9)]

    def draw(self):
        self.screen.fill((255, 255, 255))
        for i in range(10):
            line_thickness = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.height // 9), (self.width, i * self.height // 9), line_thickness)
            pygame.draw.line(self.screen, (0, 0, 0), (i * self.width // 9, 0), (i * self.width // 9, self.height), line_thickness)

        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        if self.selected_cell:
            self.selected_cell.selected = False
        self.selected_cell = self.cells[row][col]
        self.selected_cell.selected = True

    def click(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            row = y // (self.height // 9)
            col = x // (self.width // 9)
            return row, col
        return None

    def clear(self):
        if self.selected_cell and self.original_board[self.selected_cell.row][self.selected_cell.col] == 0:
            self.selected_cell.set_cell_value(0)
            self.selected_cell.set_sketched_value(0)

    def sketch(self, value):
        if self.selected_cell:
            self.selected_cell.set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell and self.original_board[self.selected_cell.row][self.selected_cell.col] == 0:
            self.selected_cell.set_cell_value(value)
            self.update_board()

    def reset_to_original(self):
        for row in range(9):
            for col in range(9):
                self.cells[row][col].set_cell_value(self.original_board[row][col])
                self.cells[row][col].set_sketched_value(0)

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def update_board(self):
        self.board_values = [[cell.value for cell in row] for row in self.cells]

    def find_empty(self):
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].value == 0:
                    return row, col
        return None

    def check_board(self):
        for row in range(9):
            for col in range(9):
                num = self.board_values[row][col]
                if num == 0:
                    return False
                self.board_values[row][col] = 0
                if not self.is_valid(row, col, num):
                    return False
                self.board_values[row][col] = num
        return True

    def is_valid(self, row, col, num):

        for c in range(9):
            if self.board_values[row][c] == num:
                return False

        for r in range(9):
            if self.board_values[r][col] == num:
                return False

        box_row = row - row % 3
        box_col = col - col % 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if self.board_values[r][c] == num:
                    return False

        return True


if __name__ == "__main__":
    main()

