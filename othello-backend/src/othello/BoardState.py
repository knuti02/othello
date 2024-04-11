from Color import Color
from OthelloBoard import OthelloBoard

from collections import defaultdict

from Directions import Directions

class BoardState:
    def __init__(self, board, current_player):
        """
        Initializes the BoardState object with the provided board and current player.

        Args:
            board (OthelloBoard): The Othello game board.
            current_player (Color): The current player's color (Color.BLACK or Color.WHITE).
        """
        self.board = board
        self.current_player = current_player
        
        # Basically a map which stores the pieces of each color
        self.places_pieces_map = defaultdict(list)
        self.places_pieces_map[Color.BLACK] = []
        self.places_pieces_map[Color.WHITE] = []
        
        # Caches to clear after each move
        # To avoid recalculating the same thing multiple times
        # Though it adds a bit of memory overhead, I think it's worth it
        self.can_flank_in_direction_cache = {}
        self.capturable_squares_cache = {Color.BLACK: set(), Color.WHITE: set()} # Stores the capturable squares for each color at the current state
        self.valid_moves_cache = {Color.BLACK: set(), Color.WHITE: set()} # Stores the valid moves for each color at the current state

    def init(self, current_player=Color.BLACK):
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
                self.places_pieces_map[square.color].append(square)
        

    def get_valid_moves(self, current_player) -> set:
        """
        Returns a set of valid moves given the current board state.

        Returns:
            set: A set containing valid moves (empty squares where a piece can be placed).
        """
        if self.valid_moves_cache[current_player]:
            return self.valid_moves_cache[current_player]
        # Get the target color
        target_color = Color.WHITE if current_player == Color.BLACK else Color.BLACK
        # Initialize the set of valid moves
        init_valid_moves = set()
        # Populate the initial valid moves
        self.populate_initial_valid_moves(init_valid_moves, target_color)
        # Filter the final valid moves
        valid_moves = self.filter_final_valid_moves(init_valid_moves, target_color)
        # Cache the result
        self.valid_moves_cache[current_player] = valid_moves
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
            raise ValueError("Not a valid move!")

        # Place the piece on the square
        square.set_color(self.current_player)
        # Update the places_pieces_map
        self.places_pieces_map[self.current_player].append(square)
        for neighbor in square.neighbors:
            direction = self.board.get_direction_of_neighbor(square, neighbor)
            if self.can_flank_in_direction(neighbor, direction, target_color):
                self.flip_pieces(square, direction, target_color)

        # The move was successful, so clear caches
        self.can_flank_in_direction_cache.clear()
        self.valid_moves_cache[Color.WHITE].clear()
        self.valid_moves_cache[Color.BLACK].clear()
        self.capturable_squares_cache[Color.WHITE].clear()
        self.capturable_squares_cache[Color.BLACK].clear()
        
        # We need to update the stability of every square that was affected by the move
        self.chain_update_stability(square)
        
        # Finnaly done, switch the player
        self.set_player(target_color)


    # All the functions below are helper functions for the methods above, 
    # except for print_get_valid_moves which is for debugging purposes
    
    # Populates the initial valid moves by adding all the empty squares that are neighbors to the target color.
    # This reduces the number of minimum squares to check for valid moves, as we only need to check the neighbors 
    # of the target color, instead of all the empty squares.
    def populate_initial_valid_moves(self, init_valid_moves, target_color):
        for square in self.places_pieces_map[target_color]:
            init_valid_moves.update(square.neighbor_map[Color.EMPTY])

    # Filters the final valid moves by checking if the square is a valid move
    def filter_final_valid_moves(self, init_valid_moves, target_color):
        final_valid_moves = set()
        for square in init_valid_moves:
            if self.is_valid_move(square, target_color):
                final_valid_moves.add(square)
        
        opponent_color = Color.WHITE if target_color == Color.BLACK else Color.BLACK
        print("CURRENTLY CAPTURABLE BY" , opponent_color, ":")
        for square in self.capturable_squares_cache[opponent_color]:
            print(square)
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
            #print("HIT: ", current_square , " from ", start_square, " in ", direction, " with ", target_color)
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
            # Fix an edge-case bug where the stability of the square is not updated in time
            # if self.is_safe_square(current_square):
            #     current_square.stability = 1
            # update the places_pieces_map
            self.places_pieces_map[target_color].remove(current_square)
            self.places_pieces_map[self.current_player].append(current_square)

    # Steps:
    # Place the new piece on the board.
    # Update stability of the square where the piece is placed.
    # Enqueue/update neighbors of the newly placed piece.
    # Dequeue from the queue and update stability of neighbors.
    # Repeat steps 3-4 until the queue is empty or stability updates cease.
    def chain_update_stability(self, square, queue = []):
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
                # If the neighbor is already visited, then continue
                if neighbor in visited:
                    continue
                # Safe squares can be ignored as they can never change stability
                if neighbor.stability == 1:
                    continue
                
                old_stability = neighbor.stability
                self.update_stability(neighbor)
                new_stability = neighbor.stability
                
                # If the stability has not changed, then continue
                # This is because, if we have reached the end of updating the stability chain
                # we should not need to update the rest of the chain to reduce the number of updates
                if old_stability == new_stability:
                    continue
                
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
        
        # First check: north or south. One of them must be a wall or a safe square, otherwise it's not safe
        north_square = self.board.get_neighboring_square_direction(square, Directions.NORTH)
        south_square = self.board.get_neighboring_square_direction(square, Directions.SOUTH)
        if (not ((
            north_square is None or (north_square.color == self.current_player and north_square.stability == 1)
        ) or (
            south_square is None or (south_square.color == self.current_player and south_square.stability == 1)
        ))):
            return False
        
        # Then east or west, same concept as above
        east_square = self.board.get_neighboring_square_direction(square, Directions.EAST)
        west_square = self.board.get_neighboring_square_direction(square, Directions.WEST)
        if (not ((
            east_square is None or (east_square.color == self.current_player and east_square.stability == 1)
        ) or (
            west_square is None or (west_square.color == self.current_player and west_square.stability == 1)
        ))):
            return False
        
        # Then north-east or south-west, same concept as above
        north_east_square = self.board.get_neighboring_square_direction(square, Directions.NORTH_EAST)
        south_west_square = self.board.get_neighboring_square_direction(square, Directions.SOUTH_WEST)
        if (not ((
            north_east_square is None or (north_east_square.color == self.current_player and north_east_square.stability == 1)
        ) or (
            south_west_square is None or (south_west_square.color == self.current_player and south_west_square.stability == 1)
        ))):
            return False
        
        # Finally, north-west or south-east, same concept as above
        north_west_square = self.board.get_neighboring_square_direction(square, Directions.NORTH_WEST)
        south_east_square = self.board.get_neighboring_square_direction(square, Directions.SOUTH_EAST)
        if (not ((
            north_west_square is None or (north_west_square.color == self.current_player and north_west_square.stability == 1)
        ) or (
            south_east_square is None or (south_east_square.color == self.current_player and south_east_square.stability == 1)
        ))):
            return False
        
        # If all the above conditions are met, then the square is safe
        return True
    
    def is_unstable_square(self, square):
        # Two ways of defining an unstable square:
        # First way: if a square is capturable by the opponent, then it's unstable
        # Second way: if a square is in valid moves, see if after that move is done wether the square is capturable by the opponent

        # Find valid moves for opponent, this will init the caches and give us capturable squares 
        opponent_color = Color.WHITE if square.color == Color.BLACK else Color.BLACK
        # get_valid_moves will update the capturable_squares_cache for opponent color
        _ = self.get_valid_moves(opponent_color)
        if square in self.capturable_squares_cache[opponent_color]:
            return True

        
        return False

    def set_player(self, color):
        self.current_player = color
        
        
    # Prints the valid moves for play in the console
    def print_get_valid_moves(self):
        valid_moves = self.get_valid_moves(self.current_player)
        print("VALID MOVES: ")
        for move in valid_moves:
            print(move)
        
        
if __name__ == "__main__":
    board = OthelloBoard(8, 8)
    game = BoardState(board, Color.BLACK)
    game.init()
    print(game.board)
    while True:
        game.print_get_valid_moves()
        print("\nChoose square to place (row,col)")
        coords = input()
        parts = coords.split(",")
        row = int(parts[0].strip())
        col = int(parts[1].strip())
        game.place_piece(row, col)
        print(game.board)
