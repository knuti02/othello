

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
        self.black_board = 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        self.white_board = 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000
        self.board = {'black': self.black_board, 'white': self.white_board}
        
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
        
    def flip_piece(self, position, from_player, to_player) -> None:
        """
        Flips a piece on the board.
        I.e., changes the color of the piece.
        For example, if the piece is white it will become black.
        Effectively, this means that the piece is removed from the from_player and added to the to_player.
        
        :param position (int): The position of the piece to flip.
        :param from_player (str): The player who's piece to flip.
        :param to_player (str): The player who's piece the flipped piece will belong to.
        
        :return (None): None
        """
        # Remove the piece from the from_player
        self.board[from_player] &= ~position
        # Add the piece to the to_player
        self.board[to_player] |= position

        
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
    
    def get_neighbors_of_player(self, player, target, pre_defined_playerboard = None) -> int:
        """
        Get the neighbors of the player's pieces.
        I.e., get the empty squares that are neighbors of the player's pieces.
        
        :param player (str): The player whose neighbors we want to get
        :param target (str): The player whose type of neighbor we want to get (opposing player or empty)
        :param pre_defined_playerboard (int): A pre-defined player board to use instead of getting it from the board.
        
        :return (int): The neighbors of the player's pieces as a bitboard.
        """
        if pre_defined_playerboard is None:
            player_board = self.get_board(player)
        else:
            player_board = pre_defined_playerboard
        target_board = self.get_board(target)
        
        # For each direction, shift the player_board one step in that direction and & with the target_board
        north_board = (player_board >> 8) & target_board
        south_board = (player_board << 8) & target_board
        west_board = (player_board >> 1) & target_board
        east_board = (player_board << 1) & target_board
        north_east_board = (player_board >> 7) & target_board
        north_west_board = (player_board >> 9) & target_board
        south_east_board = (player_board << 9) & target_board
        south_west_board = (player_board << 7) & target_board
        
        # Combine all the boards
        return north_board | south_board | east_board | west_board | north_east_board | north_west_board | south_east_board | south_west_board
    
    def get_bit_position(self, row, col) -> int:
        """
        Gets bit position based on row and col.
        The bit position is the position of the bit in the bitboard.
        
        :param row (int): The row to translate.
        :param col (int): The column to translate.
        
        :return (int): The bit position.
        """
        return row * 8 + col
    
    def get_direction_of_neighbor(self, origin, target) -> str:
        """
        Returns the direction of the neighbor.
        
        :param origin (int): The bitboard of origin.
        :param target (int): The bitboard of target.
        
        :return (str): The direction of the neighbor.
        """
        # Find difference of bit positions
        target_position = (target & -target).bit_length() - 1
        origin_position = (origin & -origin).bit_length() - 1
        diff = target_position - origin_position

        direction_map = {
            -8: 'north',
            8: 'south',
            -1: 'west',
            1: 'east',
            -7: 'north_east',
            -9: 'north_west',
            9: 'south_east',
            7: 'south_west'
        }
        
        return direction_map.get(diff, "Invalid direction")

    
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