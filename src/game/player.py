class Player:

    def __init__(self, symbol: str = "X") -> None:
        if symbol not in ["X", "O"]:
            raise ValueError("Invalid symbol")
        self.__symbol = symbol
        pass

    def get_symbol(self) -> str:
        return self.__symbol

    def play(self, row: int, col: int, game) -> None:
        game.get_board().set_player(row, col, self.__symbol)
