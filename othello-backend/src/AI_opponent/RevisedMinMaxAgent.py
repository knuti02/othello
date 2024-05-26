import random
import numpy as np

class MinMaxAgent:
    def __init__(self, cache):
        self.cache = cache
        
    def get_best_move(self, gamestate, evaluation_function, depth = 5, alpha=-float('inf'), beta=float('inf'), is_maximizing=True, player=None, beta_features=False):            
        # Base case
        if depth == 0 or gamestate.game_over:
            opponent = 'black' if player == 'white' else 'white'
            value = evaluation_function(gamestate, player, opponent, beta_features = beta_features)
            return value, None
        
        player = gamestate.current_player

        # Represent the gamestate as a string of the pieces' names
        # Used for caching
        board = (player, gamestate.board.get_board('black'), gamestate.board.get_board('white'))
        if board in self.cache:
            depth_searched, value, best_move = self.cache[board]
            if depth_searched >= depth:
                if best_move is None:
                    print("Error: best_move is None in cache. Exiting...")
                    exit(1)
                return value, best_move
        
        max_value = float('-inf')
        min_value = float('inf')

        valid_moves = gamestate.get_valid_moves(player)
        valid_moves = gamestate._bitboard_to_rowcol(valid_moves)
        if len(valid_moves) == 0:
            valid_moves = ["skip"]
            
        best_move = random.choice(valid_moves)

        for move in valid_moves:
            if move == "skip":
                gamestate.skip_turn()
            else:
                valid = gamestate.make_move(move[0], move[1])
                if not valid:
                    print(f"An error occurred. Valid moves for player {player}:")
                    print(valid_moves)
                    print("Gamestate: ")
                    print(gamestate.board)
                    print("Exiting...")
                    exit(1)
            
            value, _ = self.get_best_move(gamestate, evaluation_function, depth - 1, alpha, beta, not is_maximizing, player, beta_features = beta_features)
            
            gamestate.undo_move()

            if is_maximizing:
                if value > max_value:
                    max_value = value
                    best_move = move
                alpha = max(max_value, value)
            else:
                if value < min_value:
                    min_value = value
                    best_move = move
                beta = min(min_value, value)

            if beta <= alpha:
                break

        if is_maximizing:
            self.cache[board] = depth, max_value, best_move
            return max_value, best_move
        else:
            self.cache[board] = depth, min_value, best_move
            return min_value, best_move
        
    def clear_cache(self):
        self.cache.clear()
        
