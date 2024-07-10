from .Board import Board
import time

class GameState:
    """
    A class to represent the state of the Othello game.
    This class is responsible for the rules and logic of the game.
    It contains the board as a class and the current player.
    """
    
    def __init__(self, include_stability=True, gamestate=None):
        self.board = Board()
        self.game_over = False
        self.winner = None
        self.current_turn = 0
        # In case we want to initialize the gamestate with a specific state
        if gamestate is not None:
            print("Initializing gamestate with custom gamestate")
            self.board.board['black'] = gamestate[0]
            self.board.board['white'] = gamestate[1]
            self.current_player = gamestate[2]
            self.target_player = 'black' if self.current_player == 'white' else 'white'   
            self.game_over = gamestate[3]   
            self.current_turn = gamestate[4]

        else:
            self.current_player = 'black'
            self.target_player = 'white'
            self.board.place_piece(3, 3, 'white')
            self.board.place_piece(4, 4, 'white')
            self.board.place_piece(3, 4, 'black')
            self.board.place_piece(4, 3, 'black')
    
        self.directions = {
            "north": -8,
            "south": 8,
            "west": -1,
            "east": 1,
            "north_west": -9,
            "north_east": -7,
            "south_west": 7,
            "south_east": 9
        }
        
        self.wraparound_masks = {
            'north': 0b00000000_11111111_11111111_11111111_11111111_11111111_11111111_11111111,
            'south': 0b11111111_11111111_11111111_11111111_11111111_11111111_11111111_00000000,
            'east': 0b11111110_11111110_11111110_11111110_11111110_11111110_11111110_11111110,
            'west': 0b01111111_01111111_01111111_01111111_01111111_01111111_01111111_01111111,
            'north_east': 0b00000000_11111110_11111110_11111110_11111110_11111110_11111110_11111110,
            'north_west': 0b00000000_01111111_01111111_01111111_01111111_01111111_01111111_01111111,
            'south_east': 0b11111110_11111110_11111110_11111110_11111110_11111110_11111110_00000000,
            'south_west': 0b01111111_01111111_01111111_01111111_01111111_01111111_01111111_00000000
        }
        
        self.valid_moves_bitboard_cache = {'black': 0, 'white': 0}
        self.player_can_capture_cache = {'black': 0, 'white': 0}
        
        self.history = []
        self.include_stability = include_stability
        if self.include_stability and gamestate is not None:
            self._update_stability()
    
    
    def get_valid_moves(self, player) -> int:
        """
        Given a player, returns the valid moves for that player in the current state.
        The valid moves are returned as a bitboard where 1 represents a valid move.
        Based on: https://core.ac.uk/download/pdf/33500946.pdf
        
        :param player: The player whose valid moves to return as a string.
        
        :return: The valid moves for the player as a bitboard (integer).
        """
        # Check if we have the valid moves in the cache, in which case we return it to save time
        if self.valid_moves_bitboard_cache[player] != 0:
            return self.valid_moves_bitboard_cache[player]
        target_player = 'black' if player == 'white' else 'white'
        
        player_board = self.board.get_board(player)
        target_board = self.board.get_board(target_player)
        empty_board = self.board.get_board('empty')
        
        # Go through every direction
        valid_moves = 0
        capturable_pieces = 0 # Pieces that can be captured used for stability
        
        for direction, shift in self.directions.items():
            potentially_capturable = 0
            mask = self.wraparound_masks[direction]
            can_place_in_direction = False
            candidate_moves = self._shift_bitboard_direction(player_board, shift) & target_board & mask
            
            while candidate_moves > 0:
                valid_placements = self._shift_bitboard_direction(candidate_moves, shift) & empty_board & mask
                if valid_placements > 0: # We can place a piece in this direction, which is important for stability
                    can_place_in_direction = True
                valid_moves |= valid_placements
                potentially_capturable |= candidate_moves
                candidate_moves = self._shift_bitboard_direction(candidate_moves, shift) & target_board & mask
                
            if can_place_in_direction: # If we can place a piece in this direction, we can capture pieces
                capturable_pieces |= potentially_capturable # Update the capturable pieces
        # Add to the cache
        self.valid_moves_bitboard_cache[player] = valid_moves
        self.player_can_capture_cache[player] = capturable_pieces
        return valid_moves
        
    
    def make_move(self, row, col) -> bool:
        """
        Given a row and col, make a move for the current player.
        The move is assumed to be valid.
        
        :param row: The row to place the piece, (0-7)
        :param col: The col to place the piece, (A-H)
        
        :return: True if the move was successful, False otherwise.
        """
        col = ord(col) - 65
        move_bitboard = self._translate_rowcol_to_bitboard(row, col)
        if move_bitboard & self.get_valid_moves(self.current_player) == 0:
            print("Illegal move")
            print(f"{self.current_player} attempted move: {row, col}")
            return False
        
        # Move was successful
        self.pass_count = 0
        self.current_turn += 1
        self.history.append(self._generate_current_history())
        
        self.board.place_piece(row, col, self.current_player)
        player_bitboard = self.board.get_board(self.current_player)
        target_bitboard = self.board.get_board(self.target_player)   
        
        for direction, shift in self.directions.items():
            mask = self.wraparound_masks[direction]
            init_move = self._shift_bitboard_direction(move_bitboard, shift) & target_bitboard & mask
            if init_move == 0:
                continue
            captured = init_move
            for _ in range(5):
                old_captured = captured
                captured |= self._shift_bitboard_direction(captured, shift) & target_bitboard & mask
                if old_captured == captured:
                    break
            if self._shift_bitboard_direction(captured, shift) & player_bitboard & mask > 0:
                self.board.flip_piece(captured, self.target_player, self.current_player)
        
        self.next_turn()
        return True
    
    def skip_turn(self) -> None:
        self.history.append(self._generate_current_history())
        self.next_turn()
                
    def undo_move(self) -> None:
        if len(self.history) == 0:
            print("At the start of the game, can't undo")
            return
        
        if self.game_over:
            self.game_over = False
            self.winner = None
        
        self.current_turn -= 1
        
        last_state = self.history.pop()
        self.board.board['black'] = last_state['board'][0]
        self.board.board['white'] = last_state['board'][1]
        self.valid_moves_bitboard_cache['black'] = last_state['valid_moves'][0]
        self.valid_moves_bitboard_cache['white'] = last_state['valid_moves'][1]
        self.player_can_capture_cache['black'] = last_state['player_can_capture'][0]
        self.player_can_capture_cache['white'] = last_state['player_can_capture'][1]
        self.board.safe_board['black'] = last_state['safe_board'][0]
        self.board.safe_board['white'] = last_state['safe_board'][1]
        self.board.unstable_board['black'] = last_state['unstable_board'][0]
        self.board.unstable_board['white'] = last_state['unstable_board'][1]
        self.next_turn()
        
    def next_turn(self) -> None:
        self.capturable_squares_bitboard_cache = {'black': 0, 'white': 0}
        self.valid_moves_bitboard_cache = {'black': 0, 'white': 0}
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        self.target_player = 'black' if self.current_player == 'white' else 'white'
        if self.include_stability:
            self._update_stability()   
            
        # Check if game is over
        if self._is_game_over():
            self._set_game_over()
            return 
    
    def _generate_current_history(self) -> dict:
        current_history = {}
        current_history['board'] = (self.board.get_board('black'), self.board.get_board('white'))
        current_history['valid_moves'] = (self.valid_moves_bitboard_cache['black'], self.valid_moves_bitboard_cache['white'])
        current_history['player_can_capture'] = (self.player_can_capture_cache['black'], self.player_can_capture_cache['white'])
        current_history['safe_board'] = (self.board.safe_board['black'], self.board.safe_board['white'])
        current_history['unstable_board'] = (self.board.unstable_board['black'], self.board.unstable_board['white'])
        
        return current_history
    
    def _is_game_over(self) -> bool:
        player_is_empty = ((bin(self.board.get_board('black')).count('1') == 0) or 
                           (bin(self.board.get_board('white')).count('1') == 0))
        is_empty_board_zero = len(self._bitboard_to_rowcol(self.board.get_board('empty'))) == 0
        is_both_players_depleted_moves = (self.get_valid_moves('black') == 0 and self.get_valid_moves('white') == 0)
        is_game_over = is_empty_board_zero or player_is_empty or is_both_players_depleted_moves
        return is_game_over
    
    def _set_game_over(self) -> None:
        black_score = bin(self.board.get_board('black')).count('1')
        white_score = bin(self.board.get_board('white')).count('1')
        if black_score > white_score:
            self.winner = 'black'
        elif white_score > black_score:
            self.winner = 'white'
        else:
            self.winner = 'draw'
        self.game_over = True
    
    def _update_stability(self) -> None:
        """
        Stability is defined in three categories:
        - Safe: A piece that can't ever be flipped in an ancestor state.
        - Unstable: A piece that, in this state, can be flipped.
        - Stable: A piece that is not safe or unstable. In other words, it can be flipped in the future.
        
        The Board class has two bitboards that represent the safe and unstable pieces.
        Stable can be derived from these two bitboards.
        """
        self._update_safe('black')
        self._update_safe('white')
        
        self._update_unstable('black', 'white')
        self._update_unstable('white', 'black')

    def _update_safe(self, player) -> None:
        """
        Is a potentially expensive operation, at least in the current implementation.
        However, it is required for the stability calculation.
        The algorithm is relatively complex, but it is based on the following:
         - A corner piece is always safe.
         - Edges "built" from the corners are safe.
         - All other pieces are safe if their immediate neighbor in all 4 opposing directions are safe.
        """
        player_board = self.board.get_board(player)
        player_corners = player_board & self.board.corners
        if player_corners == 0:
            return
        
        safe_board = player_corners
        
        # Check edges, for each cardinal direction
        for direction in ['north', 'south', 'west', 'east']:
            candidates = player_corners
            shift = self.directions[direction]
            for i in range(6):
                edge = self._shift_bitboard_direction(candidates, shift) & player_board
                if edge == 0:
                    if i > 0:
                        print(f"Found safe edge(s) in direction {direction} for {player} in {i} iterations")
                    break
                #print(f"Edge getting added: {bin(edge)} in direction {direction} for {player}")
                candidates |= edge
            safe_board |= candidates
        
        # See if any of the edges were added as safe, if not we can early return
        if safe_board == player_corners:
            return
        
        # Now find the rest
        iter = 0
        while True:
            old_safe_board = safe_board
            safe_board |= (
                (self._shift_bitboard_direction(safe_board, self.directions['north']) | 
                 self._shift_bitboard_direction(safe_board, self.directions['south'])) &
                (self._shift_bitboard_direction(safe_board, self.directions['west']) |
                 self._shift_bitboard_direction(safe_board, self.directions['east'])) &
                (self._shift_bitboard_direction(safe_board, self.directions['north_west']) |
                 self._shift_bitboard_direction(safe_board, self.directions['south_east'])) &
                (self._shift_bitboard_direction(safe_board, self.directions['north_east']) |
                 self._shift_bitboard_direction(safe_board, self.directions['south_west'])) &
                player_board
            )
            
            if old_safe_board == safe_board:
                #print(f"Found safe board for {player} in {iter} iterations")
                break
            iter += 1
            
        self.board.safe_board[player] = safe_board
        
    def _update_unstable(self, player, opponent) -> None:
        """
        An unstable piece is a piece that can be flipped in the current state.
        To do this, we need to find all pieces that can be captured in the current state.
        This is done in the get_valid_moves method, and we can use the cached value.
        The reason we do it this way is to avoid recalculating the same thing multiple times.
        Though readability is sacrificed, considering this is a bitboard implementation of Othello,
        readability is already massacred.
        """
        self.get_valid_moves(player) # This will update the cache and mark all opponent pieces that can be captured
        self.board.unstable_board[opponent] = self.player_can_capture_cache[player] # The opponent's pieces that can be captured are unstable
        
    def _shift_bitboard_direction(self, bitboard, shift) -> None:
        return (bitboard << shift) if shift > 0 else (bitboard >> abs(shift))
    
    def _translate_rowcol_to_bitboard(self, row, col) -> int:
        return 1 << (row * 8 + col)
    
    def _bitboard_to_rowcol(self, bitboard) -> list:
        rowcol = [(i // 8, chr((i % 8) + 65)) for i in range(64) if bitboard & (1 << i)]
        return rowcol
            

# if __name__ == "__main__":
#     import time
#     def benchmark(game_state, iterations=100_000):
#         start = time.time()   
#         for _ in range(iterations):
#             game_state.make_move(3, 'C')
#             game_state.make_move(2, 'C')
#             game_state.make_move(2, 'D')
#             game_state.undo_move()
#             game_state.make_move(1, 'C')
#             game_state.undo_move()
#             game_state.undo_move()
#             game_state.undo_move()
            
#         end = time.time()
#         return end - start

#     for i in range(5):
#         print(f"Run {i + 1}")
#         # Initialize game states
#         print("Running benchmarks...")
#         stability_game_state = GameState(include_stability=True)
#         standard_game_state = GameState(include_stability=False)

#         # Run benchmarks
#         print("Stability game state")
#         original_time = benchmark(stability_game_state)
#         print(f"Seconds: {original_time:.4f}")
#         print("Standard game state")
#         new_time = benchmark(standard_game_state)
#         print(f"Seconds: {new_time:.4f}")

# if __name__ == "__main__":
#     gamestate = GameState()
#     print(gamestate.board)
#     while True:
#         print(f"Current player: {gamestate.current_player}")
#         print("Valid moves: ")
#         print(gamestate._bitboard_to_rowcol(gamestate.get_valid_moves(gamestate.current_player)))
#         if gamestate.get_valid_moves(gamestate.current_player) == 0:
#             print("No valid moves, skipping turn")
#             gamestate.skip_turn()
#             continue
#         move = input("Enter rowcol (number+letter in one): ")
#         if move == 'undo':
#             gamestate.undo_move()
#             print(gamestate.board)
#             continue
#         try:
#             row = int(move[0])
#             col = move[1].upper()
#         except:
#             print("Invalid input")
#             continue
        
#         print(f"Making move {row}, {col}")
#         gamestate.make_move(row, col)
#         print(gamestate.board)
#         print("Safe board black")
#         print(bin(gamestate.board.safe_board['black']))
#         print("Safe board white")
#         print(bin(gamestate.board.safe_board['white']))
