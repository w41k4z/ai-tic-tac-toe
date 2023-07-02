from game.board import Board
from game.player import Player
from game.ai import AI
import tkinter as tk


class TicTacToe:

    def __init__(self, player_choice: int) -> None:
        self.__board = Board()
        self.__player = Player("X" if player_choice == 1 else "O")
        self.__ai = AI("O" if player_choice == 1 else "X")
        self.__player_turn = True if player_choice == 1 else False

    def get_board(self) -> Board:
        return self.__board

    def has_won(self, symbol: str) -> bool:
        return self.__board.has_won(symbol)

    def player_has_won(self) -> bool:
        return self.__board.has_won(self.__player.get_symbol())

    def ai_has_won(self) -> bool:
        return self.__board.has_won(self.__ai.get_symbol())

    def is_over(self) -> bool:
        return self.player_has_won() or self.ai_has_won() or self.__board.is_full()

    def start(self):

        def on_click(row, col):
            if not self.is_over():
                if self.__player_turn:
                    self.__board.set_player(
                        row, col, self.__player.get_symbol())
                    buttons[row][col]["text"] = self.__player.get_symbol()
                    self.__player_turn = False

                    # ai turn
                    if not self.is_over():
                        ai_best_move = self.__ai.get_best_move(self)
                        self.__board.set_player(
                            ai_best_move[0], ai_best_move[1], self.__ai.get_symbol())
                        buttons[ai_best_move[0]][ai_best_move[1]
                                                 ]["text"] = self.__ai.get_symbol()
                        self.__player_turn = True

        # Create the main window
        window = tk.Tk()

        # Create buttons for the tic-tac-toe board
        buttons = []
        for row in range(3):
            button_row = []
            for col in range(3):
                button = tk.Button(window, text=" ", width=10, height=5,
                                   command=lambda r=row, c=col: on_click(r, c))
                button.grid(row=row, column=col, padx=5, pady=5)

                button_row.append(button)
            buttons.append(button_row)

        # Start the main event loop
        window.mainloop()


tic_tac_toe = TicTacToe(1)
tic_tac_toe.start()
