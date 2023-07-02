class Board:

    def __init__(self) -> None:
        self.__board = [[" " for _ in range(3)] for _ in range(3)]
        pass

    def set_player(self, row: int, col: int, player_symbol: str) -> None:
        if self.__board[row][col] != " ":
            raise ValueError("Invalid move")
        self.__board[row][col] = player_symbol

    def undo_move(self, row: int, col: int):
        self.__board[row][col] = " "

    def is_full(self):
        for row in self.__board:
            for col in row:
                if col == " ":
                    return False
        return True

    def has_won(self, player_symbol: str):
        win_state = [
            # horizontal
            [self.__board[0][0], self.__board[0][1], self.__board[0][2]],
            [self.__board[1][0], self.__board[1][1], self.__board[1][2]],
            [self.__board[2][0], self.__board[2][1], self.__board[2][2]],
            # vertical
            [self.__board[0][0], self.__board[1][0], self.__board[2][0]],
            [self.__board[0][1], self.__board[1][1], self.__board[2][1]],
            [self.__board[0][2], self.__board[1][2], self.__board[2][2]],
            # diagonal
            [self.__board[0][0], self.__board[1][1], self.__board[2][2]],
            [self.__board[0][2], self.__board[1][1], self.__board[2][0]]
        ]

        return True if [player_symbol, player_symbol, player_symbol] in win_state else False

    def get_empty_cell(self) -> list:
        empty_cells = []
        for row in range(3):
            for col in range(3):
                if self.__board[row][col] == " ":
                    empty_cells.append([row, col])
        return empty_cells

    def get_depth(self) -> int:
        return len(self.get_empty_cell())
