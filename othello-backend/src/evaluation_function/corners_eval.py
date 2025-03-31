import math
from .constants import CORNERS_CORNER_WEIGHT, CORNERS_POTENTIAL_WEIGHT, CORNERS_STANDARD_WEIGHT, CORNERS_DYNAMIC_MAX_WEIGHT, CORNERS_DYNAMIC_MIDPOINT, CORNERS_DYNAMIC_STEEPNESS

def corners_heuristics_weight_function(
        placed_pieces: int, 
        maximum_weight: int = CORNERS_DYNAMIC_MAX_WEIGHT,  
        midpoint: int = CORNERS_DYNAMIC_MIDPOINT, 
        steepness: float = CORNERS_DYNAMIC_STEEPNESS
    ) -> float:
    return (-1 * maximum_weight) / (1 + math.e ** (-1* steepness * (placed_pieces - midpoint))) + maximum_weight

def corners_eval(gamestate, player, opponent, placed_pieces, dynamic_weight = True, corners_hyperparameters = None):
    """
    Evaluation function for corners; scores based on how many corners you have 
    and how many corners you are able to capture in a given gamestate
    """
    corners = gamestate.board.corners
    def corners_value(player) -> int:
        player_board = gamestate.board.get_board(player)
        corners_value = CORNERS_CORNER_WEIGHT * bin(player_board & corners).count('1')
        potential_corners = CORNERS_POTENTIAL_WEIGHT * bin(gamestate.get_valid_moves(player) & corners).count('1')

        return corners_value + potential_corners
    
    if corners_hyperparameters is not None:
        maximum_weight = corners_hyperparameters.get('maximum_weight', CORNERS_DYNAMIC_MAX_WEIGHT)
        midpoint = corners_hyperparameters.get('midpoint', CORNERS_DYNAMIC_MIDPOINT)
        steepness = corners_hyperparameters.get('steepness', CORNERS_DYNAMIC_STEEPNESS)
        weight = corners_heuristics_weight_function(placed_pieces, maximum_weight, midpoint, steepness) if dynamic_weight else CORNERS_STANDARD_WEIGHT
    else:
        weight = corners_heuristics_weight_function(placed_pieces) if dynamic_weight else CORNERS_STANDARD_WEIGHT
    
    current_corners_value = corners_value(player)
    opponent_corners_value = corners_value(opponent)
    
    corners_denominator = abs(current_corners_value) + abs(opponent_corners_value)
    # prevent division by zero
    if corners_denominator == 0:
        return 0
    
    combined_corners_value = weight * ((current_corners_value - opponent_corners_value) / (corners_denominator))
    
    return combined_corners_value