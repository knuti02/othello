from Color import Color

class Square:
    def __init__(self, row, col, color=Color.EMPTY, stability=0):
        """
        Initialize a new Square instance.

        :param row: The row position of the square.
        :param col: The column position of the square.
        :param color: The color of the square, if any.
        :param stability: The stability of the square. Used for heuristic evaluation.
        """
        self.row = row
        self.col = col
        self.color = color
        self.stability = stability
        self.neighbors = []
        self.neighbor_map = {Color.BLACK: [], Color.WHITE: [], Color.EMPTY: []}

    def add_neighbor(self, neighbor):
        """
        Add a neighbor to the current square. The neighbor must not already be in the list.
        This method also adds the neighbor to the neighbor map, keyed by its color.

        :param neighbor: The neighbor square to be added.
        :raises ValueError: If the target square (neighbor) is already a neighbor of this square.
        """
        if neighbor in self.neighbors:
            raise ValueError("Target square (neighbor) is already a neighbor of this square.")
        self.neighbors.append(neighbor)
        self.neighbor_map[neighbor.color].append(neighbor)

    def set_color(self, color):
        """
        Set the color of the current square. This method also updates the neighborMap of the
        current square's neighbors to reflect the change in color for this square.

        :param color: The color to set the current square to.
        """
        self.color = color
        for neighbor in self.neighbors:
            neighbor.update_neighbor_map(self)
            
    def update_neighbor_map(self, neighbor):
        """
        Updates the neighborMap of the current square. This method assumes that the neighborMap
        of the current square has already been initialized. It updates the map to reflect any
        change in the color of the neighbor squares.

        :param neighbor: The square to be updated in the neighborMap.
        """
        removeFrom = self.get_key_from_square(neighbor)
        self.neighbor_map[removeFrom].remove(neighbor)
        self.neighbor_map[neighbor.color].append(neighbor)

    def get_key_from_square(self, neighbor):
        """
        Based on the square's position, determine the key (color) which it is currently
        associated with in the neighborMap.

        :param neighbor: The neighbor square whose key is to be determined.
        :return: The color key if found, None otherwise.
        """
        for color in Color:
            if neighbor in self.neighbor_map[color]:
                return color
        return None

    def __str__(self):
        """
        Returns a string representation of the square, indicating its color and position.

        :return: A string representation of the square.
        """
        return f"{self.color.name} square at ({self.row},{self.col})"