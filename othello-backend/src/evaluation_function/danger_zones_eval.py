import math
from constants import DANGER_ZONES_ORANGE_PENALTY, DANGER_ZONES_RED_PENALTY, DANGER_ZONES_STANDARD_WEIGHT, DANGER_ZONES_DYNAMIC_MAX_WEIGHT, DANGER_ZONES_DYNAMIC_MIDPOINT, DANGER_ZONES_DYNAMIC_STEEPNESS

def danger_zones_heuristics_weight_function(
        placed_pieces: int, 
        maximum_weight: int = DANGER_ZONES_DYNAMIC_MAX_WEIGHT,  
        midpoint: int = DANGER_ZONES_DYNAMIC_MIDPOINT, 
        steepness: float = DANGER_ZONES_DYNAMIC_STEEPNESS
    ) -> float:

    return (maximum_weight) / (1 + math.e ** (-1 * steepness * (placed_pieces - midpoint)))

def danger_zones_eval(gamestate, player, opponent, placed_pieces, dynamic_weight = True):
    """
    Evaluation function to make the model avoid areas generally seen as disadvantageous
    """
    orange_zone_penalty = DANGER_ZONES_ORANGE_PENALTY
    red_zone_penalty = DANGER_ZONES_RED_PENALTY
    
    def evaluate_danger_zones(player, opponent) -> int:
        player_board = gamestate.board.get_board(player)
        all_occupied_corners = gamestate.board.corners & (player_board | gamestate.board.get_board(opponent))
        
        # Orange zones are the edge squares directly adjacent to the corners
        orange_zone = 0b01000010_10000001_00000000_00000000_00000000_00000000_10000001_01000010
        orange_zone = orange_zone & ~(all_occupied_corners << 1 | all_occupied_corners >> 1 | 
                                     all_occupied_corners << 8 | all_occupied_corners >> 8)
        # Red zones are the squares on the diagonals directly adjacent to the corners
        red_zone = 0b00000000_01000010_00000000_00000000_00000000_00000000_01000010_00000000
        red_zone = red_zone & ~(all_occupied_corners << 9 | all_occupied_corners >> 9 | 
                          all_occupied_corners << 7 | all_occupied_corners >> 7)
        
        orange_zone_value = bin(player_board & orange_zone).count('1')
        red_zone_value = bin(player_board & red_zone).count('1')
        
        # Apply the penalties
        return orange_zone_value * orange_zone_penalty + red_zone_value * red_zone_penalty
    
    # Apply dynamic weight to the danger zones
    weight = danger_zones_heuristics_weight_function(placed_pieces) if dynamic_weight else DANGER_ZONES_STANDARD_WEIGHT
    
    # Evaluate the player's danger zone value
    player_danger_zones_value = evaluate_danger_zones(player, opponent)

    # Combine the danger zones evaluation with the dynamic weight
    return weight * player_danger_zones_value
