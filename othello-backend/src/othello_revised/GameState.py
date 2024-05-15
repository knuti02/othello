from Board import Board

class GameState:
    """
    A class to represent the state of the Othello game.
    This class is responsible for the rules and logic of the game.
    It contains the board as a class and the current player.
    """
    
    def __init__(self):
        self.board = Board()
        self.current_player = 'black'
        self.target_player = 'white'
        self.pass_count = 0
        self.game_over = False
        self.winner = None
        
        self.board.place_piece(3, 3, 'white')
        self.board.place_piece(4, 4, 'white')
        self.board.place_piece(3, 4, 'black')
        self.board.place_piece(4, 3, 'black')
    
        # For the directions
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
        
        self.opposite_directions = {
            'north': 'south',
            'south': 'north',
            'east': 'west',
            'west': 'east',
            'north_east': 'south_west',
            'north_west': 'south_east',
            'south_east': 'north_west',
            'south_west': 'north_east'
        }
        
        self.capturable_squares_bitboard_cache = {'black': 0, 'white': 0}
        self.valid_moves_bitboard_cache = {'black': 0, 'white': 0}
    
    
    def get_valid_moves(self, player) -> int:
        """
        Given a player, returns the valid moves for that player in the current state.
        The valid moves are returned as a bitboard where 1 represents a valid move.
        
        :param player: The player whose valid moves to return as a string.
        
        :return: The valid moves for the player as a bitboard (integer).
        """
        # Check if we have the valid moves in the cache, in which case we return it to save time
        if self.valid_moves_bitboard_cache[player] != 0:
            return self.valid_moves_bitboard_cache[player]
        
        target_player = 'black' if player == 'white' else 'white'
        # First get the initial valid moves
        init_valid_moves = self._get_init_valid_moves(target_player)
        # Then reduce to valid moves
        valid_moves = self._get_final_valid_moves(init_valid_moves, player, target_player)
        return valid_moves
    
    def make_move(self, row, col) -> bool:
        """
        Given a row and col, make a move for the current player.
        The move is assumed to be valid.
        
        :param row: The row to place the piece.
        :param col: The col to place the piece.
        """
        # Translate col to number
        col = ord(col) - 65
        # Translate the row, col to a bitboard
        move_bitboard = self._translate_rowcol_to_bitboard(row, col)
        # Get valid moves for the current player
        valid_moves_mask = self.get_valid_moves(self.current_player)
        # Check if the move is valid
        if move_bitboard & valid_moves_mask == 0:
            print("Invalid move")
            return False
        # Move is valid, place the piece
        self.board.place_piece(row, col, self.current_player)
        # Flip the pieces
        self._flip_pieces(move_bitboard, self.current_player, self.target_player)
        return True
        
    def next_turn(self) -> None:
        # Clear the caches
        self.capturable_squares_bitboard_cache = {'black': 0, 'white': 0}
        self.valid_moves_bitboard_cache = {'black': 0, 'white': 0}
        
        # Switch the players
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        self.target_player = 'black' if self.current_player == 'white' else 'white'
    
    def _get_init_valid_moves(self, target_player) -> int:
        """
        Look at only empty squares that are neighbors of the opponent player's pieces.
        This reduces the amount of squares to look at from all empty squares to 
        only the empty squares adjacent to a the neighbors of the opponent player's pieces.
        
        :param target_player: The player whose empty neighbors we need to find.
        
        :return: The valid moves for the player as a set of tuples.
        """
        empty_neighbors_map = self.board.get_neighbors_of_player(target_player, 'empty')
        return empty_neighbors_map
    
    def _get_final_valid_moves(self, init_valid_moves, player, target_player) -> int:
        """
        Given the initial valid moves, reduce it to the final valid moves.
        This is done by looking at the directions of the opponent's pieces and checking if there are any pieces
        that can be flipped in that direction.
        
        :param init_valid_moves: The initial valid moves as a set of tuples.
        :param player: The player whose valid moves to return as a string.
        
        :return: The final valid moves for the player as a set of tuples.
        """
        valid_moves = 0
        for direction in self.directions:
            valid_moves |= self._traverse_direction(direction, init_valid_moves, player, target_player)
            
        return valid_moves
        
    def _traverse_direction(self, direction, bitboard, player, target_player) -> int:
        """
        Traverse in a given direction from the origin bitboard and check if we can flip any pieces.
        Return the positions of the valid moves as a bitboard.
        
        :param direction: The direction to traverse in.
        :param bitboard: The origin bitboard.
        :param player: The player whose pieces to check.
        :param target_player: The player whose pieces to flip.
        
        :return: The positions of the valid moves as a bitboard.
        """
        # Where we can place the pieces
        allowed_positions = 0
        # Which pieces can be flipped
        flippable_positions = 0
        
        # Get the direction shift
        shift = self.directions[direction]
        
        # In a given direction from the origin bitboard, the immediate neighbor must be the target player
        bitboard_copy = self._shift_bitboard_direction(bitboard, shift)
        bitboard_copy &= self.board.get_board(target_player)
        if bitboard_copy == 0: # If there are no target player pieces in the direction, we can't traverse
            return 0
        
        # Find opposite direction and appropriate shift
        opposite_direction = self.opposite_directions[direction]
        opposite_shift = self.directions[opposite_direction]
        
        # After this, the next square can continue to be the target player or the current player
        # However, if it's an empty square (or the wall), we can't traverse in this direction
        iteration = 1
        while bitboard_copy > 0 and (bitboard_copy & self.board.get_board('empty')) == 0:
            bitboard_copy = self._shift_bitboard_direction(bitboard_copy, shift)
            # See if we hit target player's piece, in which case we can flip the pieces and 
            # add the position to the allowed positions
            if (bitboard_copy & self.board.get_board(player)) != 0:
                # Find the position
                position = bitboard_copy & self.board.get_board(player)
                # Shift it back to the original position
                for _ in range(iteration):
                    position = self._shift_bitboard_direction(position, opposite_shift)
                    # Add the position to the flippable positions
                    flippable_positions |= position
                # Add onle last shift
                position = self._shift_bitboard_direction(position, opposite_shift)
                # Add the position to the allowed positions 
                allowed_positions |= position

            # See if we hit another target player piece
            # We & with the target player board to check for non-zero results, 
            # and update the bitboard if we hit another target player piece
            if (bitboard_copy & self.board.get_board(target_player)) != 0:
                bitboard_copy &= self.board.get_board(target_player)
            # Update the iteration
            iteration += 1
        
        # Add to the caches
        self.capturable_squares_bitboard_cache[player] |= flippable_positions
        self.valid_moves_bitboard_cache[player] |= allowed_positions
        return allowed_positions
    
    def _flip_pieces(self, move_bitboard, player, target) -> None:
        """
        Given a valid move bitboard, find the pieces to flip and flip them.
        
        :param move_bitboard: The move bitboard.
        :param player: The player who made the move.
        """
        
        # First find which directions to traverse
        # Can reduce this by only checking directions with immediate enemy neighbors
        directions = []
        
        # Extract the neighbors
        neighbors_bitboard = self.board.get_neighbors_of_player(player, target, move_bitboard)
        neighbors_bitboard_list = []
        # Expand them to individual bitboards
        while neighbors_bitboard != 0:
            rightmost_bit = neighbors_bitboard & -neighbors_bitboard
            neighbors_bitboard_list.append(rightmost_bit)
            neighbors_bitboard &= ~rightmost_bit
        # Find the directions
        for neighbor in neighbors_bitboard_list:
            directions.append(self.board.get_direction_of_neighbor(move_bitboard, neighbor))
        # Traverse in the directions and flip the pieces
        for direction in directions:
            self._flip_pieces_direction(move_bitboard, direction, player, target)
            
    def _flip_pieces_direction(self, move_bitboard, direction, player, target) -> None:
        """
        Given a move bitboard, traverse in a direction and flip the pieces.
        
        :param move_bitboard: The move bitboard.
        :param direction: The direction to traverse.
        :param player: The player who made the move.
        """
        # Get the direction shift
        shift = self.directions[direction]
        
        # In a given direction from the origin bitboard, the immediate neighbor must be the target player
        bitboard_copy = self._shift_bitboard_direction(move_bitboard, shift)
        bitboard_copy &= self.board.get_board(target)
        if bitboard_copy == 0: # If there are no target player pieces in the direction, we can't traverse
            return
        
        iteration = 1
        while bitboard_copy > 0 and (bitboard_copy & self.board.get_board('empty')) == 0:
            bitboard_copy = self._shift_bitboard_direction(bitboard_copy, shift)
            # See if we hit target player's piece, in which case we can flip the pieces
            if (bitboard_copy & self.board.get_board(player)) != 0:
                # Find the position
                position = bitboard_copy & self.board.get_board(player)
                # Shift it back to the original position
                for _ in range(iteration):
                    position = self._shift_bitboard_direction(position, -shift)
                    # Flip the piece from target to player
                    self.board.flip_piece(position, from_player=target, to_player=player)
            
            # See if we hit another target player piece
            # We & with the target player board to check for non-zero results, 
            # and update the bitboard if we hit another target player piece
            if (bitboard_copy & self.board.get_board(target)) != 0:
                bitboard_copy &= self.board.get_board(target)
            # Update the iteration
            iteration += 1

    def _shift_bitboard_direction(self, bitboard, shift) -> None:
        return (bitboard << shift) if shift > 0 else (bitboard >> abs(shift))
    
    def _translate_rowcol_to_bitboard(self, row, col) -> int:
        """
        Given a row and col, convert it to a bitboard.
        Row should be numbered from 0 to 7.
        Col should be numbered from 0 to 7.
        
        :param row: The row to convert.
        :param col: The col to convert.
        
        :return: The bitboard representation of the row, col.
        """
        return 1 << (row * 8 + col)
    
    def _bitboard_to_rowcol(self, bitboard) -> list:
        """
        Given a bitboard, convert it to a list of row, col tuples.
        Row should be numbered from 0 to 7 from top to bottom.
        Col should be labeled from A to H from left to right.
        Helper function for debugging.
        
        :param bitboard: The bitboard to convert.
        
        :return: A list of row, col tuples.
        """
        rowcol = []
        for i in range(64):
            if bitboard & (1 << i):
                row = i // 8
                col = i % 8
                rowcol.append(str(row) + chr(col + 65))
        return rowcol
                    

if __name__ == "__main__":
    gamestate = GameState()
    print(gamestate.board)
    while True:
        print(f"Current player: {gamestate.current_player}")
        print("Valid moves: ")
        print(gamestate._bitboard_to_rowcol(gamestate.get_valid_moves(gamestate.current_player)))
        move = input("Enter rowcol (number+letter in one): ")
        row = int(move[0])
        col = move[1].upper()
        
        success = gamestate.make_move(row, col)
        if not success:
            continue
        print(gamestate.board)
        gamestate.next_turn()