import random

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
        #valid_moves = gamestate._bitboard_to_rowcol(valid_moves)
        valid_moves = self.order_moves(valid_moves)
        
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

    
    def order_moves(self, moves_bitboard):
        """
        Move ordering is difficult to implement in Othello
        I opted for a static board representing the general value of each square
        This isnt ideal, however should be sufficent for ordering moves at least a little bit
        Some tests showed that this ordering improved time performance by up to 40%
        """
        def _bitboard_to_rowcol(bitboard) -> list:
            rowcol = [(i // 8, chr((i % 8) + 65)) for i in range(64) if bitboard & (1 << i)]
            return rowcol
        
        # highest priority moves
        corner_bitboard = 0b10000001_00000000_00000000_00000000_00000000_00000000_00000000_10000001 & moves_bitboard
        corner_moves = _bitboard_to_rowcol(corner_bitboard)
        
        edge_bitboard = 0b00111100_00000000_10000001_10000001_10000001_10000001_00000000_01111110 & moves_bitboard
        edge_moves = _bitboard_to_rowcol(edge_bitboard)
        
        center_bitboard = 0b00000000_00000000_00111100_00111100_00111100_00111100_00000000_00000000 & moves_bitboard
        center_moves = _bitboard_to_rowcol(center_bitboard)
        
        semi_edge_bitboard = 0b00000000_00111100_01000010_01000010_01000010_01000010_00111100_00000000 & moves_bitboard
        semi_edge_moves = _bitboard_to_rowcol(semi_edge_bitboard)
        
        orange_zone_bitboard = 0b01000010_10000001_00000000_00000000_00000000_00000000_10000001_01000010 & moves_bitboard
        orange_zone_moves = _bitboard_to_rowcol(orange_zone_bitboard)
        
        red_zone_bitboard = 0b00000000_01000010_00000000_00000000_00000000_00000000_01000010_00000000 & moves_bitboard
        red_zone_moves = _bitboard_to_rowcol(red_zone_bitboard)
        
        moves_ordered = corner_moves + edge_moves + center_moves + semi_edge_moves + orange_zone_moves + red_zone_moves
        return moves_ordered
        