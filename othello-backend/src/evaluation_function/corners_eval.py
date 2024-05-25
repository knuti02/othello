import math

def corners_heuristics_weight_function(placed_pieces: int, maximum_weight: int = 100,  midpoint: int = 35, steepness: float = 0.5) -> float:
    return (-1 * maximum_weight) / (1 + math.e ** (-1* steepness * (placed_pieces - midpoint))) + maximum_weight

def corners_eval(gamestate, player, opponent, placed_pieces, dynamic_weight = True):
    corners = gamestate.board.corners
    def corners_value(player) -> int:
        player_board = gamestate.board.get_board(player)
        corners_value = bin(player_board & corners).count('1')

        return corners_value
    
    weight = corners_heuristics_weight_function(placed_pieces) if dynamic_weight else 30
    
    current_corners_value = corners_value(player)
    opponent_corners_value = corners_value(opponent)
    
    corners_denominator = abs(current_corners_value) + abs(opponent_corners_value)
    # prevent division by zero
    if corners_denominator == 0:
        return 0
    
    combined_corners_value = weight * ((current_corners_value - opponent_corners_value) / (corners_denominator)) 
    
    return combined_corners_value