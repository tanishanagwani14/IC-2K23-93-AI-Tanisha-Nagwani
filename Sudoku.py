def print_board(board):
    print("\n" + "=" * 25)
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- " * 11)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            print(f"{board[i][j]} ", end="")
        print()
    print("=" * 25 + "\n")

def is_valid(board, row, col, num):
    # Check row and column constraints
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    # Check 3x3 subgrid constraint
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:  # Find unassigned cell
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0  # Backtrack
                return False
    return True

def get_user_board():
    print("--- CUSTOM SUDOKU INPUT ---")
    print("Enter the board row by row (9 numbers per row separated by spaces). Use '0' for empty cells.\n")

    board = []
    for i in range(9):
        while True:
            try:
                row_input = input(f"Enter Row {i + 1}: ").strip().split()
                if len(row_input) != 9:
                    print("Error: Exactly 9 numbers required. Try again.")
                    continue
                row = [int(n) for n in row_input]
                if any(n < 0 or n > 9 for n in row):
                    print("Error: Numbers must be between 0 and 9. Try again.")
                    continue
                board.append(row)
                break
            except ValueError:
                print("Error: Invalid integers entered. Try again.")
    return board

if __name__ == "__main__":
    print("--- SUDOKU SOLVER (BACKTRACKING) ---")
    choice = input("Do you want to enter a custom board? (y/n): ").strip().lower()

    if choice == 'y':
        board = get_user_board()
    else:
        print("\nLoading default sample Sudoku puzzle...")
        board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]

    print("\nInitial Sudoku Board:")
    print_board(board)

    if solve_sudoku(board):
        print("Solved Sudoku Board:")
        print_board(board)
    else:
        print("No solution exists for the given Sudoku puzzle!")
        