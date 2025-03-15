import math
from constants import STABILITY_SAFE_WEIGHT, STABILITY_STABLE_WEIGHT, STABILITY_UNSTABLE_WEIGHT, STABILITY_STANDARD_WEIGHT, STABILITY_DYNAMIC_MAX_WEIGHT, STABILITY_DYNAMIC_MIDPOINT, STABILITY_DYNAMIC_STEEPNESS

def stability_heuristics_weight_function(
        placed_pieces: int, 
        maximum_weight: int = STABILITY_DYNAMIC_MAX_WEIGHT,  
        midpoint: int = STABILITY_DYNAMIC_MIDPOINT, 
        steepness: float = STABILITY_DYNAMIC_STEEPNESS
    ) -> float:
    
    return (-1*maximum_weight) / (1 + math.e ** (-1 * steepness * (placed_pieces - midpoint))) + maximum_weight

def stability_eval(gamestate, player, opponent, placed_pieces, dynamic_weight = True):
    """
    Evaluation function for stability (can never be captured, 
    can be captured but not in given gamestate, can be captured in current gamestate)
    """
    def get_stability(player) -> int:
        player_board = gamestate.board.get_board(player)
        number_of_player_pieces = bin(player_board).count('1')
        safe_board = gamestate.board.safe_board[player]
        unstable_board = gamestate.board.unstable_board[player]
        stable_board = player_board & ~(safe_board | unstable_board)
        
        stability = (
            (bin(safe_board).count('1') * STABILITY_SAFE_WEIGHT) / number_of_player_pieces + 
            bin(stable_board).count('1') * STABILITY_STABLE_WEIGHT + 
            bin(unstable_board).count('1') * STABILITY_UNSTABLE_WEIGHT / number_of_player_pieces
        )
        
        return stability
    
    # Calculate weight using the defined weight function
    weight = stability_heuristics_weight_function(placed_pieces) if dynamic_weight else STABILITY_STANDARD_WEIGHT
    
    player_stability = get_stability(player)
    opponent_stability = get_stability(opponent)
    
    stability_denominator = abs(player_stability) + abs(opponent_stability)
    # prevent division by zero
    if stability_denominator == 0:
        return 0
    
    # Calculate combined stability using the weighted difference between current player's and opponent's stability
    combined_stability = weight * ((player_stability - opponent_stability) / stability_denominator)
    return combined_stability