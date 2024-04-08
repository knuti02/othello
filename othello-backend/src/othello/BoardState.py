from Color import Color
from OthelloBoard import OthelloBoard

from collections import defaultdict

class BoardState:
    def __init__(self, board, current_player):
        self.board = board
        self.current_player = current_player
        self.places_pieces_map = defaultdict(list)
        self.places_pieces_map[Color.BLACK] = []
        self.places_pieces_map[Color.WHITE] = []

    def init(self):
        # Set the initial pieces' color
        self.board.get_square(3, 3).set_color(Color.WHITE)
        self.board.get_square(3, 4).set_color(Color.BLACK)
        self.board.get_square(4, 3).set_color(Color.BLACK)
        self.board.get_square(4, 4).set_color(Color.WHITE)

        # Add the squares to the map
        for row in [3, 4]:
            for col in [3, 4]:
                square = self.board.get_square(row, col)
                self.places_pieces_map[square.color].append(square)

    def get_valid_moves(self):
        init_valid_moves = set()
        target_color = Color.WHITE if self.current_player == Color.BLACK else Color.BLACK

        # Populate initial valid moves
        self.populate_initial_valid_moves(init_valid_moves, target_color)

        # Filter valid moves away
        return self.filter_final_valid_moves(init_valid_moves, target_color)
    
    def print_get_valid_moves(self):
        valid_moves = self.get_valid_moves()
        for move in valid_moves:
            print(move)

    def place_piece(self, row, col):
        target_color = Color.WHITE if self.current_player == Color.BLACK else Color.BLACK
        square = self.board.get_square(row, col)
        if square not in self.get_valid_moves():
            raise ValueError("Not a valid move!")

        square.set_color(self.current_player)
        self.places_pieces_map[self.current_player].append(square)
        for neighbor in square.neighbors:
            direction = self.board.get_direction_of_neighbor(square, neighbor)
            if self.can_flank_in_direction(neighbor, direction, target_color):
                self.flip_pieces(square, direction, target_color)

        self.set_player(target_color)

    def populate_initial_valid_moves(self, init_valid_moves, target_color):
        for square in self.places_pieces_map[target_color]:
            init_valid_moves.update(square.neighbor_map[Color.EMPTY])

    def filter_final_valid_moves(self, init_valid_moves, target_color):
        final_valid_moves = set()
        for square in init_valid_moves:
            if self.is_valid_move(square, target_color):
                final_valid_moves.add(square)
        return final_valid_moves

    def is_valid_move(self, square, target_color):
        neighbors = square.neighbor_map[target_color]
        for neighbor in neighbors:
            direction = self.board.get_direction_of_neighbor(square, neighbor)
            if self.can_flank_in_direction(neighbor, direction, target_color):
                return True
        return False

    def can_flank_in_direction(self, start_square, direction, target_color):
        current_square = start_square
        while True:
            current_square = self.board.get_neighboring_square_direction(current_square, direction)
            if current_square is None or current_square.color == Color.EMPTY:
                return False
            elif current_square.color == target_color:
                continue
            return True  # Hit the player's color; valid

    def flip_pieces(self, start_square, direction, target_color):
        current_square = start_square
        while True:
            current_square = self.board.get_neighboring_square_direction(current_square, direction)
            if current_square.color == target_color:
                current_square.set_color(self.current_player)
                self.places_pieces_map[target_color].remove(current_square)
                self.places_pieces_map[self.current_player].append(current_square)
            else:
                return

    def set_player(self, color):
        self.current_player = color
        
        
if __name__ == "__main__":
    board = OthelloBoard(8, 8)
    game = BoardState(board, Color.BLACK)
    game.init()
    print(game.board)
    while True:
        print("Valid moves: ")
        game.print_get_valid_moves()
        print("\nChoose square to place (row,col)")
        coords = input()
        parts = coords.split(",")
        row = int(parts[0].strip())
        col = int(parts[1].strip())
        game.place_piece(row, col)
        print(game.board)
