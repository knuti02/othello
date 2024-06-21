class Board:
    """
    A class to represent the Othello board.
    Will be represented using bitboards.
    Should be able to specify the size of the board 
    in case we want to play on a board that is not 8x8.
    
    This class is not responsible for the rules or logic of the game,
    only the representation, updating and querying of the board.
    In addition it contains some helper functions to make it easier to work with the board,
    such as getting the neighboring squares of a square.
    """
    def __init__(self):
        self.board = {
            'black': 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000, 
            'white': 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        }
        
        self.safe_board = {
            'black': 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000,
            'white': 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000,
        }
        
        self.unstable_board = {
            'black': 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000,
            'white': 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        }
        
        self.corners = 0b10000001_00000000_00000000_00000000_00000000_00000000_00000000_10000001
        
    def get_board(self, player) -> int:
        """
        Returns the board of the player.
        If player is "empty" it will return the empty squares.
        
        :param player (str): The player whose board to return.
        
        :return (int): The board of the player.
        """
        if player == 'empty':
            return ~(self.board['black'] | self.board['white'])
        return self.board[player]
        
    def place_piece(self, row, col, player) -> None:
        """
        Places a piece on the board.
        
        :param row (int): The row of the piece to place.
        :param col (int): The column of the piece to place
        :param player (str): The player who places the piece.
        
        :return (None): None
        """
        bit_position = row * 8 + col
        self.board[player] |= 1 << bit_position
        
    def flip_piece(self, bitboard, from_player, to_player) -> None:
        """
        Flips a piece on the board.
        I.e., changes the color of the piece.
        For example, if the piece is white it will become black.
        Effectively, this means that the piece is removed from the from_player and added to the to_player.
        
        :param bitboard (int): The bitboard of the piece(s) to flip.
        :param from_player (str): The player who's piece(s) to flip.
        :param to_player (str): The player who's piece(s) the flipped piece(s) will belong to.
        
        :return (None): None
        """
        self.board[from_player] &= ~bitboard
        self.board[to_player] |= bitboard

        
    def get_color_of_piece(self, row, col) -> str:
        """
        Returns the color of the piece at the specified position.
        Checks each board for a non-zero result by & the board with a 
        bitboard with only the bit at the specified position set to 1.
        
        :param row (int): The row of the piece to check.
        :param col (int): The column of the piece to check.
        
        :return (str): The color of the piece.
        """
        bit_position = row * 8 + col
        if self.board['black'] & (1 << bit_position):
            return 'black'
        elif self.board['white'] & (1 << bit_position):
            return 'white'
        return 'empty'

    
    def __str__(self):
        color_map = {
            'empty': "\033[90m",  # Grey
            'white': "\033[97m",  # White
            'black': "\033[40m"   # Black
        }
        reset_color = "\033[0m"
        
        sb = []
        for row in range(8):
            sb.append(f"{row}|")
            sb.append("|".join([f"{color_map[self.get_color_of_piece(row, col)]}{self.get_color_of_piece(row, col)}{reset_color}" for col in range(8)]) + "|")
            sb.append("\n")
        col_header = "    " + "     ".join([str(col_index) for col_index in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')])
        return col_header + "\n" + ''.join(sb)