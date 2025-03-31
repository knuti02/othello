import math
from .constants import WEDGES_WEDGE_WEIGHT, WEDGES_POTENTIAL_WEIGHT, WEDGES_STANDARD_WEIGHT, WEDGES_DYNAMIC_MAX_WEIGHT, WEDGES_DYNAMIC_MIDPOINT, WEDGES_DYNAMIC_STEEPNESS

def wedge_heuristics_weight_function(
        placed_pieces: int, 
        maximum_weight: int = WEDGES_DYNAMIC_MAX_WEIGHT,  
        midpoint: int = WEDGES_DYNAMIC_MIDPOINT, 
        steepness: float = WEDGES_DYNAMIC_STEEPNESS
    ) -> float:
    return maximum_weight / (1 + math.e ** (-steepness * (placed_pieces - midpoint)))

def wedges_eval(gamestate, player, opponent, placed_pieces, dynamic_weight=True, wedges_hyperparameters=None):
    """
    Evaluates wedge formations for the given gamestate.
    
    """
    wedge_modifier = WEDGES_WEDGE_WEIGHT
    potential_wedge_modifier = WEDGES_POTENTIAL_WEIGHT

    def evaluate_wedges(player, opponent):
        player_board = gamestate.board.get_board(player)
        # Evaluate horizontal and vertical wedges.
        horizontal = (player_board << 1) & (player_board >> 1)
        vertical = (player_board << 8) & (player_board >> 8)
        player_wedges = (bin(horizontal).count('1') + bin(vertical).count('1')) * potential_wedge_modifier

        opponent_board = gamestate.board.get_board(opponent)
        opponent_horizontal = (opponent_board << 1) & (opponent_board >> 1)
        opponent_vertical = (opponent_board << 8) & (opponent_board >> 8)
        opponent_wedges = (bin(opponent_horizontal).count('1') + bin(opponent_vertical).count('1')) * wedge_modifier

        return player_wedges + opponent_wedges

    if wedges_hyperparameters is not None:
        maximum_weight = wedges_hyperparameters.get('maximum_weight', WEDGES_DYNAMIC_MAX_WEIGHT)
        midpoint = wedges_hyperparameters.get('midpoint', WEDGES_DYNAMIC_MIDPOINT)
        steepness = wedges_hyperparameters.get('steepness', WEDGES_DYNAMIC_STEEPNESS)
        weight = wedge_heuristics_weight_function(placed_pieces, maximum_weight, midpoint, steepness) if dynamic_weight else WEDGES_STANDARD_WEIGHT
    else:
        weight = wedge_heuristics_weight_function(placed_pieces) if dynamic_weight else WEDGES_STANDARD_WEIGHT

    player_wedge_score = evaluate_wedges(player, opponent)
    opponent_wedge_score = evaluate_wedges(opponent, player)
    denom = abs(player_wedge_score) + abs(opponent_wedge_score)
    if denom == 0:
        return 0
    combined_wedges = weight * ((player_wedge_score - opponent_wedge_score) / denom)
    return combined_wedges
