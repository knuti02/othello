import math
from constants import MOBILITY_STANDARD_WEIGHT, MOBILITY_DYNAMIC_MAX_WEIGHT, MOBILITY_DYNAMIC_MIDPOINT, MOBILITY_DYNAMIC_STEEPNESS

def mobility_heuristics_weight_function(
        placed_pieces: int, 
        maximum_weight: int = MOBILITY_DYNAMIC_MAX_WEIGHT,  
        midpoint: int = MOBILITY_DYNAMIC_MIDPOINT, 
        steepness: float = MOBILITY_DYNAMIC_STEEPNESS
    ) -> float:
    
    return (-1*maximum_weight) / (1 + math.e ** (-1 * steepness * (placed_pieces - midpoint))) + maximum_weight

def mobility_eval(gamestate, player, opponent, placed_pieces, dynamic_weight = True, mobility_hyperparameters = None):
    """
    Evaluation function for mobility; i.e., how many moves available given current gamestate.
    """
    def get_mobility(player):
        player_valid_moves = bin(gamestate.get_valid_moves(player)).count('1')
        opponent_valid_moves = bin(gamestate.get_valid_moves(opponent)).count('1')
        all_valid_moves = player_valid_moves + opponent_valid_moves
        # Prevent division by zero
        if all_valid_moves == 0:
            return 0
        mobility = player_valid_moves / all_valid_moves
        return mobility
    
    # Use custom hyperparameters for dynamic weight if provided
    if mobility_hyperparameters is not None:
        maximum_weight = mobility_hyperparameters.get('maximum_weight', MOBILITY_DYNAMIC_MAX_WEIGHT)
        midpoint = mobility_hyperparameters.get('midpoint', MOBILITY_DYNAMIC_MIDPOINT)
        steepness = mobility_hyperparameters.get('steepness', MOBILITY_DYNAMIC_STEEPNESS)
        weight = mobility_heuristics_weight_function(placed_pieces, maximum_weight, midpoint, steepness) if dynamic_weight else MOBILITY_STANDARD_WEIGHT
    else:
        weight = mobility_heuristics_weight_function(placed_pieces) if dynamic_weight else MOBILITY_STANDARD_WEIGHT
    
    player_mobility = get_mobility(player)
    opponent_mobility = get_mobility(opponent)
    
    mobility_denominator = abs(player_mobility) + abs(opponent_mobility)
    if mobility_denominator == 0:
        return 0
    
    combined_mobility = weight * ((player_mobility - opponent_mobility) / mobility_denominator)
    return combined_mobility