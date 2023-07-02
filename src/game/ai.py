from game.player import Player
from joblib import load


class AI(Player):

    def __init__(self, symbol: str, difficulty: str = "hard") -> None:
        super().__init__(symbol)
        if difficulty not in ["easy", "medium", "hard"]:
            raise ValueError("Invalid difficulty")
        self.__dificulty = difficulty
        self.__model = load("model/x_prediction_model.joblib") if symbol == "X" else load(
            "model/o_prediction_model.joblib")

    def get_best_move(self, game) -> tuple:
        if self.__dificulty == "easy":
            return self.easy_move(game)
        elif self.__dificulty == "medium":
            return self.medium_move(game)
        else:
            return self.hard_move(game)

    def easy_move(self, game):
        return self.__predict(game)

    def medium_move(self, game):
        opponent_symbol = "O" if self.get_symbol() == "X" else "X"

        # checking for a winnable move
        for empty_cell in game.get_board().get_empty_cell():
            game.get_board().set_player(
                empty_cell[0], empty_cell[1], self.get_symbol())

            if game.has_won(self.get_symbol()):
                game.get_board().undo_move(empty_cell[0], empty_cell[1])
                return empty_cell

            game.get_board().undo_move(empty_cell[0], empty_cell[1])

        # defensive move
        for empty_cell in game.get_board().get_empty_cell():
            game.get_board().set_player(
                empty_cell[0], empty_cell[1], opponent_symbol)

            if game.has_won(opponent_symbol):
                game.get_board().undo_move(empty_cell[0], empty_cell[1])
                return empty_cell

            game.get_board().undo_move(empty_cell[0], empty_cell[1])

        # creative move
        # checking for the center
        if game.get_board().is_available(1, 1):
            return [1, 1]
        else:
            # checking for the corners
            corners = [[0, 0], [0, 2], [2, 0], [2, 2]]
            for corner in corners:
                if game.get_board().is_available(corner[0], corner[1]):
                    return corner

            # checking for the sides
            sides = [[0, 1], [1, 0], [1, 2], [2, 1]]
            for side in sides:
                if game.get_board().is_available(side[0], side[1]):
                    return side

    def hard_move(self, game):
        return self.__minimax(
            game, game.get_board().get_depth(), self.get_symbol())["move"]

    def __predict(self, game):
        opponent_latest_move = game.get_board().get_array_expression()
        prediction = self.__model.predict([opponent_latest_move])[0]
        return [prediction[0], prediction[1]]

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
