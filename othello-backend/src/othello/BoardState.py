from collections import defaultdict

from .Color import Color
from .Directions import Directions
from .OthelloBoard import OthelloBoard

class BoardState:
    def __init__(self, board = OthelloBoard(8,8), current_player = Color.BLACK):
        """
        Initializes the BoardState object with the provided board and current player.

        Args:
            board (OthelloBoard): The Othello game board.
            current_player (Color): The current player's color (Color.BLACK or Color.WHITE).
        """
        self.board = board
        self.current_player = current_player
        self.skipped_turns = 0
        self.placed_piece = None
        
        # Basically a map which stores the pieces of each color
        self.player_pieces_map = defaultdict(list)
        self.player_pieces_map[Color.BLACK] = []
        self.player_pieces_map[Color.WHITE] = []
        
        # Move history; stores moves and which pieces were flipped as a result
        self.move_history = []
        
        # Caches to clear after each move
        # To avoid recalculating the same thing multiple times
        # Though it adds a bit of memory overhead, I think it's worth it
        self.can_flank_in_direction_cache = {}
        self.capturable_squares_cache = {Color.BLACK: set(), Color.WHITE: set()} # Stores the capturable squares for each color at the current state
        self.valid_moves_cache = {Color.BLACK: set(), Color.WHITE: set()} # Stores the valid moves for each color at the current state

    def init(self):
        """Sets the initial pieces on the board."""
        # Note: we cant use place_piece here because place_piece checks for valid moves which are not available yet
        # Set the initial pieces' color
        
        self.board.get_square(3, 3).set_color(Color.WHITE)
        self.board.get_square(3, 4).set_color(Color.BLACK)
        self.board.get_square(4, 3).set_color(Color.BLACK)
        self.board.get_square(4, 4).set_color(Color.WHITE)

        # Add the squares to the map
        for row in [3, 4]:
            for col in [3, 4]:
                square = self.board.get_square(row, col)
                square.stability = -1
                self.player_pieces_map[square.color].append(square)
        

    def get_valid_moves(self, player) -> set:
        """
        Returns a set of valid moves given the current board state.

        Returns:
            set: A set containing valid moves (empty squares where a piece can be placed).
        """
        if self.valid_moves_cache[player]:
            return self.valid_moves_cache[player]
        # Get the target color
        target_color = Color.WHITE if player == Color.BLACK else Color.BLACK
        # Initialize the set of valid moves
        init_valid_moves = set()
        # Populate the initial valid moves
        self.populate_initial_valid_moves(init_valid_moves, target_color)
        # Filter the final valid moves
        valid_moves = self.filter_final_valid_moves(init_valid_moves, target_color)
        if len(valid_moves) == 0:
            # Add skip to valid moves if no valid moves are available
            valid_moves.add("skip")
        # Cache the result
        self.valid_moves_cache[player] = valid_moves
        # Return the valid moves
        return valid_moves
        

    def place_piece(self, row, col):
        """
        Places a piece on the board at the specified row and column.

        Args:
            row (int): The row index.
            col (int): The column index.

        Raises:
            ValueError: If the specified move is not valid.
        """
        # Get the target color and the square you want to place the piece on
        target_color = Color.WHITE if self.current_player == Color.BLACK else Color.BLACK
        square = self.board.get_square(row, col)
        # Check if the square is in the valid moves
        if square not in self.get_valid_moves(self.current_player):
            return False

        # Add the move to the move history
        self.move_history.append((
            (square.row, square.col), [], self.placed_piece
        ))
        
        # Place the piece on the square
        square.set_color(self.current_player)
        # Update the player_pieces_map
        self.player_pieces_map[self.current_player].append(square)
        for neighbor in square.neighbors:
            direction = self.board.get_direction_of_neighbor(square, neighbor)
            if self.can_flank_in_direction(neighbor, direction, target_color):
                self.flip_pieces(square, direction, target_color)

        self.skipped_turns = 0
        self.placed_piece = square
        return True
    
    def skip_turn(self):
        self.skipped_turns += 1
    
    def next_turn(self):
        self.clear_caches()
        self.chain_update_stability(self.placed_piece)
        self.set_player(Color.WHITE if self.current_player == Color.BLACK else Color.BLACK)
    
    def is_game_over(self):
        # Case 1: No empty squares left
        if (len(self.player_pieces_map[Color.BLACK]) + len(self.player_pieces_map[Color.WHITE]) == self.board.amount_of_squares):
            return True
        # Case 2: A player has no squares left
        if (len(self.player_pieces_map[Color.BLACK]) == 0 or len(self.player_pieces_map[Color.WHITE]) == 0):
            return True
        
        # Case 3: Skipped 2 times in a row (no valid moves left for both players)
        if self.skipped_turns == 2:
            return True
        
        return False
    
    def get_winner(self):        
        black_pieces = len(self.player_pieces_map[Color.BLACK])
        white_pieces = len(self.player_pieces_map[Color.WHITE])
        if black_pieces > white_pieces:
            return Color.BLACK
        elif white_pieces > black_pieces:
            return Color.WHITE            
        return None 
    
    
    def undo_move(self):
        if not self.move_history:
            return False
        # New player is the opposite of the current player
        new_player = Color.WHITE if self.current_player == Color.BLACK else Color.BLACK
        # Get the last move
        last_move = self.move_history.pop()
        # Get the square of the last move
        square = self.board.get_square(last_move[0][0], last_move[0][1])
        
        color = square.color.name
        
        # Set the square color to empty
        square.set_color(Color.EMPTY)
        # Update stability to 0, unless it's a corner in which case it's 1
        square.stability = 1 if square in self.board.corners else 0
        # Find which player the square belonged to
        player = self.current_player if color == self.current_player.name else new_player
        # Remove the square from the player pieces map
        self.player_pieces_map[player].remove(square)
        # Find the flipped pieces
        flipped_pieces = last_move[1]
        # Flip the pieces back
        for flipped_piece in flipped_pieces:
            # Get the square object of the flipped piece
            square = self.board.get_square(flipped_piece[0], flipped_piece[1])
            # Set the color to the current player
            square.set_color(self.current_player)
            # Update the player pieces map
            self.player_pieces_map[new_player].remove(square)
            self.player_pieces_map[self.current_player].append(square)
        
        # Update placed piece
        self.placed_piece = last_move[2]
        
        return True
    
    
    # Populates the initial valid moves by adding all the empty squares that are neighbors to the target color.
    # This reduces the number of minimum squares to check for valid moves, as we only need to check the neighbors 
    # of the target color, instead of all the empty squares.
    def populate_initial_valid_moves(self, init_valid_moves, target_color):
        for square in self.player_pieces_map[target_color]:
            init_valid_moves.update(square.neighbor_map[Color.EMPTY])

    # Filters the final valid moves by checking if the square is a valid move
    def filter_final_valid_moves(self, init_valid_moves, target_color):
        final_valid_moves = set()
        for square in init_valid_moves:
            if self.is_valid_move(square, target_color):
                final_valid_moves.add(square)
        return final_valid_moves

    # Checks if the move is valid by checking if the square can flank in any direction
    # It goes through all the neighbors of the square and checks if it can flank in that direction
    def is_valid_move(self, square, target_color):
        is_valid = False
        neighbors = square.neighbor_map[target_color]
        for neighbor in neighbors:
            direction = self.board.get_direction_of_neighbor(square, neighbor)
            if self.can_flank_in_direction(neighbor, direction, target_color):
                # cant do early return because we need to cache capturable squares, therefore just mark as valid move
                is_valid = True
        return is_valid

    # Checks if the square can flank in a certain direction
    # It goes through the neighbors of the square in the direction and checks if it can flank in that direction
    def can_flank_in_direction(self, start_square, direction, target_color):
        opponent_color = Color.WHITE if target_color == Color.BLACK else Color.BLACK
        # To avoid when calculating unstable squares later
        capturable_squares = [start_square]
        # Check if the result is in the cache
        if (start_square, direction, target_color) in self.can_flank_in_direction_cache:
            return self.can_flank_in_direction_cache[(start_square, direction, target_color)]
        
        # initialize the current square to the start square
        current_square = start_square
        while True:
            # Get the next square in the direction
            current_square = self.board.get_neighboring_square_direction(current_square, direction)
            
            # If the square is None (wall), or the color is empty, then we stop flipping as it can't flank in that direction
            if current_square is None or current_square.color == Color.EMPTY:
                # Cache the result
                self.can_flank_in_direction_cache[(start_square, direction, target_color)] = False
                return False
            # If the color is the target color, continue to the next square
            elif current_square.color == target_color:
                capturable_squares.append(current_square)
                continue
            
            # If the color is the player's color, then it can flank in that direction
            # Cache the result
            self.can_flank_in_direction_cache[(start_square, direction, target_color)] = True
            self.capturable_squares_cache[opponent_color].update(capturable_squares)
            return True

    # Flips the pieces in a certain direction
    # It goes through the neighbors of the square in the direction and flips the pieces in that direction
    def flip_pieces(self, start_square, direction, target_color):
        current_square = start_square
        while True:
            # Get the next square in the direction
            current_square = self.board.get_neighboring_square_direction(current_square, direction)
            # If the square is empty, or the color is the same as the target color, then we stop flipping
            if current_square.color != target_color:
                return
            current_square.set_color(self.current_player)
            self.player_pieces_map[target_color].remove(current_square)
            self.player_pieces_map[self.current_player].append(current_square)
            
            # Add the flipped piece to the move history
            self.move_history[-1][1].append((current_square.row, current_square.col))

    # Steps:
    # Place the new piece on the board.
    # Update stability of the square where the piece is placed.
    # Enqueue/update neighbors of the newly placed piece.
    # Dequeue from the queue and update stability of neighbors.
    # Repeat steps 3-4 until the queue is empty or stability updates cease.
    def chain_update_stability(self, square, queue = []):
        # Base case for if undowing reaches start of match, i.e., square is None
        if square is None:
            # Set all pieces to unstable
            for sqr in self.board.get_all_squares():
                if sqr.color != Color.EMPTY:
                    sqr.stability = -1            
            return
        
        # Place the new piece on the board
        self.update_stability(square)
        
        # Enqueue/update neighbors of the newly placed piece
        queue = [square]
        # Set to keep track of visited squares
        visited = set()
        visited.add(square)
        while queue:
            # Dequeue from the queue
            current_square = queue.pop(0)
            for neighbor in current_square.neighbors:
                # No need to check for empty squares, as they can never change stability
                if neighbor.color == Color.EMPTY:
                    continue
                # If the neighbor is already visited, then continue
                if neighbor in visited:
                    continue
                # Safe squares can be ignored as they can never change stability
                if neighbor.stability == 1:
                    continue
                
                self.update_stability(neighbor)
                # If the stability has changed, then enqueue the neighbor
                queue.append(neighbor)
                # Mark the neighbor as visited to avoid updating it again
                visited.add(neighbor)
    
    # Updates the stability of the square
    def update_stability(self, square):
        """
        Args:
            square (Square): The square to update the stability for.
        """
        if self.is_safe_square(square):
            square.stability = 1
            for neighbor in square.neighbor_map[square.color]:
                if neighbor.stability == 1:
                    continue
                self.update_stability(neighbor)
            return
        
        if self.is_unstable_square(square):
            square.stability = -1
            return
        
        square.stability = 0
        
        
    def is_safe_square(self, square):
        # A square is safe given that, for each of it's complementary directions, 
        # all of them are other safe squares or walls
        # In this case, a complementary direction is the opposite direction another direction
        # For example, the complementary direction of NORTH is SOUTH
        # So if NORTH, WEST, NORTH_WEST and SOUTH_WEST are all safe squares or walls, then the square is safe
        
        complementary_directions = {
            Directions.NORTH: Directions.SOUTH,
            Directions.SOUTH: Directions.NORTH,
            Directions.EAST: Directions.WEST,
            Directions.WEST: Directions.EAST,
            Directions.NORTH_EAST: Directions.SOUTH_WEST,
            Directions.SOUTH_WEST: Directions.NORTH_EAST,
            Directions.NORTH_WEST: Directions.SOUTH_EAST,
            Directions.SOUTH_EAST: Directions.NORTH_WEST
        }
        
        # Check each direction
        for direction in Directions:
            complementary = complementary_directions.get(direction)
            square_in_direction = self.board.get_neighboring_square_direction(square, direction)
            complementary_square = self.board.get_neighboring_square_direction(square, complementary)
            
            if not (
                square_in_direction and (square_in_direction.color == self.current_player and square_in_direction.stability == 1)
                or
                complementary_square and (complementary_square.color == self.current_player and complementary_square.stability == 1)
            ):
                return False
        
        return True
    
    def is_unstable_square(self, square):
        # Two ways of defining an unstable square:
        # First way: if a square is capturable by the opponent, then it's unstable
        # Second way: if a square is in valid moves, see if after that move is done wether the square is capturable by the opponent

        # Find valid moves for opponent, this will init the caches and give us capturable squares 
        opponent_color = Color.WHITE if square.color == Color.BLACK else Color.BLACK
        # get_valid_moves will update the capturable_squares_cache for opponent color'
        _ = self.get_valid_moves(opponent_color)
        if square in self.capturable_squares_cache[opponent_color]:
            return True
        
        return False

    def set_player(self, color):
        self.current_player = color
        
    # Prints the valid moves for play in the console
    def print_get_valid_moves(self, player):
        valid_moves = self.get_valid_moves(player)
        for move in valid_moves:
            print(move)
            
    def clear_caches(self):
        self.can_flank_in_direction_cache.clear()
        self.valid_moves_cache[Color.WHITE].clear()
        self.valid_moves_cache[Color.BLACK].clear()
        self.capturable_squares_cache[Color.WHITE].clear()
        self.capturable_squares_cache[Color.BLACK].clear()
