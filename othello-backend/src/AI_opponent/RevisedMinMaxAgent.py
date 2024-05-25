import numpy as np

class MinMaxAgent:
    def __init__(self, cache):
        self.cache = cache
        
    def get_best_move(self, gamestate, heuristic_function, depth = 5, alpha=-float('inf'), beta=float('inf'), is_maximizing=True, player=None):            
        # Base case
        if depth == 0 or gamestate.game_over:
            opponent = 'black' if player == 'white' else 'white'
            value = heuristic_function(gamestate, player, opponent)
            return value, None
        
        player = gamestate.current_player

        # Represent the gamestate as a string of the pieces' names
        # Used for caching
        board = (player, gamestate.board.get_board('black'), gamestate.board.get_board('white'))
        if board in self.cache:
            depth_searched, value, best_move = self.cache[board]
            if depth_searched >= depth:
                return value, best_move
        
        # # Detect symmetry
        # is_symmetric, board_str = self.detect_symmetry(gamestate)
        # if is_symmetric:
        #     depth_searched, value, best_move = self.cache[board_str]
        #     if depth_searched >= depth:
        #         return value, best_move
        
        max_value = float('-inf')
        min_value = float('inf')
        best_move = None

        valid_moves = gamestate.get_valid_moves(player)
        valid_moves = gamestate._bitboard_to_rowcol(valid_moves)
        if len(valid_moves) == 0:
            valid_moves = ["skip"]

        for move in valid_moves:
            if move == "skip":
                gamestate.skip_turn()
            else:
                valid = gamestate.make_move(move[0], move[1])
                if not valid:
                    print(f"An error occurred. Valid moves for player {player}:")
                    print(valid_moves)
                    print("Exiting...")
                    exit(1)
            
            value, _ = self.get_best_move(gamestate, heuristic_function, depth - 1, alpha, beta, not is_maximizing, player)
            
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
        
    def detect_symmetry(self, gamestate):
        """
        Detects if the board is symmetric
        Rotates the board 4 times and checks if the mirrored board is in the cache
        This is incredibly useful in the early game where this often occurs,
        and has improved runtime in early stages by around 20-30%.
        
        In later stages, however, it is practically useless as the board is too complex to be mirrored.
        As such, the function is only called if fewer than 16 pieces have been placed on the board.
        (Through testing, around 12 was usually the limit where it was faster to not use 
        this function when the AI played against itself, but this number can vary depending 
        on the board state so we give some leeway with 16 pieces as the limit)
        """
        
        number_of_pieces = len(gamestate.player_pieces_map[Color.BLACK]) + len(gamestate.player_pieces_map[Color.WHITE])
        if number_of_pieces > 16:
            return False, None
        
        board = gamestate.board.board_dimension 
                
        # Rotate the board
        for _ in range(4): # Rotate the board 4 times
            rotated_board = np.rot90(board)            
            mirror_horizontal = ''.join([square.color.name[0] for row in np.flipud(rotated_board) for square in row])
            mirror_vertical = ''.join([square.color.name[0] for row in np.fliplr(rotated_board) for square in row])
            if mirror_horizontal in self.cache:
                return True, mirror_horizontal
            
            elif mirror_vertical in self.cache:
                return True, mirror_vertical
        
        return False, None

