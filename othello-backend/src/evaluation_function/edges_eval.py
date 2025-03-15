import math
from constants import EDGES_STANDARD_WEIGHT, EDGES_DYNAMIC_MAX_WEIGHT, EDGES_DYNAMIC_MIDPOINT, EDGES_DYNAMIC_STEEPNESS

def edges_heuristics_weight_function(
        placed_pieces: int, 
        maximum_weight: int = EDGES_DYNAMIC_MAX_WEIGHT,  
        midpoint: int = EDGES_DYNAMIC_MIDPOINT, 
        steepness: float = EDGES_DYNAMIC_STEEPNESS
    ) -> float:

    return maximum_weight / (1 + math.e ** (-steepness * (placed_pieces - midpoint)))

def edges_eval(gamestate, player, opponent, placed_pieces, dynamic_weight = True):
    edges = 0b00111110_00000000_10000001_10000001_10000001_10000001_00000000_00111100
    
    def evaluate_edges(player) -> int:
        player_board = gamestate.board.get_board(player)
        edges_value = bin(player_board & edges).count('1')
        
        return edges_value
    
    player_edges_value = evaluate_edges(player)
    opponent_edges_value = evaluate_edges(opponent)
    
    edges_denominator = abs(player_edges_value) + abs(opponent_edges_value)
    # prevent division by zero
    if edges_denominator == 0:
        return 0
    
    weight = edges_heuristics_weight_function(placed_pieces) if dynamic_weight else EDGES_STANDARD_WEIGHT
    
    combined_edges_value = weight * ((player_edges_value - opponent_edges_value) / (edges_denominator))
    return combined_edges_value