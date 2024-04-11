from Directions import Directions
from Color import Color
from Square import Square

class OthelloBoard:
    def __init__(self, y, x):
        corners = [(0, 0), (0, x - 1), (y - 1, 0), (y - 1, x - 1)]
        self.board_dimension = [[Square(row, col) for col in range(x)] for row in range(y)]
        for corner in corners:
            self.board_dimension[corner[0]][corner[1]].stability = 1
        
        # Add neighbors
        for row in range(y):
            for col in range(x):
                current_square = self.get_square(row, col)
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        if row + i < 0 or row + i >= y or col + j < 0 or col + j >= x:
                            continue
                        current_square.add_neighbor(self.get_square(row + i, col + j))
        
        self.corners = [(0, 0), (0, x - 1), (y - 1, 0), (y - 1, x - 1)]
        
        self.direction_map = {
            Directions.NORTH: (-1, 0),
            Directions.SOUTH: (1, 0),
            Directions.EAST: (0, -1),
            Directions.WEST: (0, 1),
            Directions.NORTH_EAST: (-1, -1),
            Directions.NORTH_WEST: (-1, 1),
            Directions.SOUTH_EAST: (1, -1),
            Directions.SOUTH_WEST: (1, 1)
        }

    def get_board_dimension(self):
        return self.board_dimension

    def get_square(self, row, col):
        try:
            return self.board_dimension[row][col]
        except IndexError:
            return None

    # Returns the neighboring square in a certain direction
    def get_neighboring_square_direction(self, square, direction):
        dir = self.direction_map[direction]
        row = square.row + dir[0]
        col = square.col + dir[1]
        if row < 0 or row >= len(self.board_dimension) or col < 0 or col >= len(self.board_dimension[0]):
            return None
        return self.get_square(square.row + dir[0], square.col + dir[1])

    # Returns the direction of the neighbor
    def get_direction_of_neighbor(self, origin, target):
        x = target.row - origin.row
        y = target.col - origin.col

        # Ugly code but is needed because of the way the directions are stored
        if x == -1 and y == 0:
            return Directions.NORTH
        elif x == 1 and y == 0:
            return Directions.SOUTH
        elif x == 0 and y == -1:
            return Directions.EAST
        elif x == 0 and y == 1:
            return Directions.WEST
        elif x == -1 and y == -1:
            return Directions.NORTH_EAST
        elif x == -1 and y == 1:
            return Directions.NORTH_WEST
        elif x == 1 and y == -1:
            return Directions.SOUTH_EAST
        elif x == 1 and y == 1:
            return Directions.SOUTH_WEST
        else:
            return None  # Should be unreachable

    def __str__(self):
        color_map = {
            Color.EMPTY: "\033[90m",  # Grey
            Color.WHITE: "\033[97m",  # White
            Color.BLACK: "\033[40m"   # Black
        }
        reset_color = "\033[0m"
        sb = []
        for row_index, row in enumerate(self.board_dimension):
            sb.append(f"{row_index}|")  # Add row index at the start of each row
            sb.append("|".join([f"{color_map[square.color]}{square.color.name + str(square.stability)}{reset_color}" for square in row]) + "|")
            sb.append("\n")
        col_header = "    " + "      ".join([str(col_index) for col_index in range(len(self.board_dimension[0]))])  # Add column headers
        return col_header + "\n" + ''.join(sb)

if __name__ == "__main__":
    board = OthelloBoard(8, 8)
    neighbors = board.get_square(0, 0).neighbors
    for neigbor in neighbors:
        print(neigbor)