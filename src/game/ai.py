from game.player import Player


class AI(Player):

    def __init__(self, symbol: str, difficulty: str = "hard") -> None:
        super().__init__(symbol)
        if difficulty not in ["easy", "medium", "hard"]:
            raise ValueError("Invalid difficulty")
        self.__dificulty = difficulty

    def get_best_move(self, game) -> tuple:
        if self.__dificulty == "easy":
            return self.easy_move(game)
        elif self.__dificulty == "medium":
            return self.medium_move(game)
        else:
            return self.hard_move(game)

    def easy_move(self, game):
        pass

    def medium_move(self, game):
        pass

    def hard_move(self, game):
        return self.__minimax(
            game, game.get_board().get_depth(), self.get_symbol())["move"]

    def __minimax(self, game, depth: int, player_symbol: str) -> int:
        opponent_symbol = "O" if player_symbol == "X" else "X"

        # initializing the worst score and move
        if player_symbol == "X":
            best = {"move": [-1, -1], "score": float("inf")}
        else:
            best = {"move": [-1, -1], "score": float("-inf")}

        # if the game is over, return the score
        if depth == 0 or game.is_over():
            if game.has_won("X"):
                return {"move": [-1, -1], "score": -1}
            elif game.has_won("O"):
                return {"move": [-1, -1], "score": 1}
            else:
                return {"move": [-1, -1], "score": 0}

        # testing every possible move
        for empty_cell in game.get_board().get_empty_cell():
            # setting the player in the empty cell
            game.get_board().set_player(
                empty_cell[0], empty_cell[1], player_symbol)

            # getting the best of the opponent from that move
            opponent_best = self.__minimax(game, depth - 1, opponent_symbol)

            # undoing the move
            game.get_board().undo_move(empty_cell[0], empty_cell[1])

            opponent_best["move"] = empty_cell

            # if the score is better than the best score, update the best score
            if player_symbol == "X":
                if opponent_best["score"] < best["score"]:
                    best = opponent_best
            else:
                if opponent_best["score"] > best["score"]:
                    best = opponent_best

        return best
