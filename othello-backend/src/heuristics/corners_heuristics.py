import math

def corners_heuristics_weight_function(placed_pieces: int, maximum_weight: int = 100,  midpoint: int = 35, steepness: float = 0.5) -> float:
    return (-1 * maximum_weight) / (1 + math.e ** (-1* steepness * (placed_pieces - midpoint))) + maximum_weight

def corners_heuristics(gamestate, placed_pieces, current_squares, opponent_squares, dynamic_weight = True):
    corners = gamestate.board.corners
    def corners_value(squares) -> int:
        corners_value = 0
        player_valid_moves = gamestate.get_valid_moves(squares[0].color)
        for corner in corners:
            # See if corner is occupied by the current player
            if corner in squares:
                corners_value += 1
                continue
            # See if player can move to the corner
            if corner in player_valid_moves:
                corners_value += 0
                continue
            # Can not occupy the corner
            corners_value -= 1

        return corners_value
    
    weight = corners_heuristics_weight_function(placed_pieces) if dynamic_weight else 30
    
    current_corners_value = corners_value(current_squares)
    opponent_corners_value = corners_value(opponent_squares)
    
    corners_denominator = abs(current_corners_value) + abs(opponent_corners_value)
    # prevent division by zero
    if corners_denominator == 0:
        return 0
    
    combined_corners_value = weight * ((current_corners_value - opponent_corners_value) / (corners_denominator)) 
    
    return combined_corners_value