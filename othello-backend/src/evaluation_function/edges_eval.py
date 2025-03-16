import math
from constants import EDGES_STANDARD_WEIGHT, EDGES_DYNAMIC_MAX_WEIGHT, EDGES_DYNAMIC_MIDPOINT, EDGES_DYNAMIC_STEEPNESS

def edges_heuristics_weight_function(
        placed_pieces: int, 
        maximum_weight: int = EDGES_DYNAMIC_MAX_WEIGHT,  
        midpoint: int = EDGES_DYNAMIC_MIDPOINT, 
        steepness: float = EDGES_DYNAMIC_STEEPNESS
    ) -> float:
    return maximum_weight / (1 + math.e ** (-steepness * (placed_pieces - midpoint)))

def edges_eval(gamestate, player, opponent, placed_pieces, dynamic_weight=True, edges_hyperparameters=None):
    """
    Evaluates edge control for the given gamestate.
    """
    edges = 0b00111110_00000000_10000001_10000001_10000001_10000001_00000000_00111100
    
    def evaluate_edges(player):
        player_board = gamestate.board.get_board(player)
        return bin(player_board & edges).count('1')
    
    if edges_hyperparameters is not None:
        maximum_weight = edges_hyperparameters.get('maximum_weight', EDGES_DYNAMIC_MAX_WEIGHT)
        midpoint = edges_hyperparameters.get('midpoint', EDGES_DYNAMIC_MIDPOINT)
        steepness = edges_hyperparameters.get('steepness', EDGES_DYNAMIC_STEEPNESS)
        weight = edges_heuristics_weight_function(placed_pieces, maximum_weight, midpoint, steepness) if dynamic_weight else EDGES_STANDARD_WEIGHT
    else:
        weight = edges_heuristics_weight_function(placed_pieces) if dynamic_weight else EDGES_STANDARD_WEIGHT

    player_edges = evaluate_edges(player)
    opponent_edges = evaluate_edges(opponent)
    denom = abs(player_edges) + abs(opponent_edges)
    if denom == 0:
        return 0
    combined_edges = weight * ((player_edges - opponent_edges) / denom)
    return combined_edges
