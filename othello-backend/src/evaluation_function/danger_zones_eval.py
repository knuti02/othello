import math
from constants import DANGER_ZONES_ORANGE_PENALTY, DANGER_ZONES_RED_PENALTY, DANGER_ZONES_STANDARD_WEIGHT, DANGER_ZONES_DYNAMIC_MAX_WEIGHT, DANGER_ZONES_DYNAMIC_MIDPOINT, DANGER_ZONES_DYNAMIC_STEEPNESS

def danger_zones_heuristics_weight_function(
        placed_pieces: int, 
        maximum_weight: int = DANGER_ZONES_DYNAMIC_MAX_WEIGHT,  
        midpoint: int = DANGER_ZONES_DYNAMIC_MIDPOINT, 
        steepness: float = DANGER_ZONES_DYNAMIC_STEEPNESS
    ) -> float:
    return maximum_weight / (1 + math.e ** (-steepness * (placed_pieces - midpoint)))

def danger_zones_eval(gamestate, player, opponent, placed_pieces, dynamic_weight=True, danger_zones_hyperparameters=None):
    """
    Evaluates danger zones, penalizing moves in risky areas near corners.
    """
    orange_zone_penalty = DANGER_ZONES_ORANGE_PENALTY
    red_zone_penalty = DANGER_ZONES_RED_PENALTY
    
    def evaluate_danger_zones(player, opponent):
        player_board = gamestate.board.get_board(player)
        all_occupied_corners = gamestate.board.corners & (player_board | gamestate.board.get_board(opponent))
        # Orange zones: edge squares adjacent to corners
        orange_zone = 0b01000010_10000001_00000000_00000000_00000000_00000000_10000001_01000010
        orange_zone = orange_zone & ~(all_occupied_corners << 1 | all_occupied_corners >> 1 | 
                                      all_occupied_corners << 8 | all_occupied_corners >> 8)
        # Red zones: diagonal squares adjacent to corners
        red_zone = 0b00000000_01000010_00000000_00000000_00000000_00000000_01000010_00000000
        red_zone = red_zone & ~(all_occupied_corners << 9 | all_occupied_corners >> 9 | 
                                all_occupied_corners << 7 | all_occupied_corners >> 7)
        orange_value = bin(player_board & orange_zone).count('1')
        red_value = bin(player_board & red_zone).count('1')
        return orange_value * orange_zone_penalty + red_value * red_zone_penalty

    if danger_zones_hyperparameters is not None:
        maximum_weight = danger_zones_hyperparameters.get('maximum_weight', DANGER_ZONES_DYNAMIC_MAX_WEIGHT)
        midpoint = danger_zones_hyperparameters.get('midpoint', DANGER_ZONES_DYNAMIC_MIDPOINT)
        steepness = danger_zones_hyperparameters.get('steepness', DANGER_ZONES_DYNAMIC_STEEPNESS)
        weight = danger_zones_heuristics_weight_function(placed_pieces, maximum_weight, midpoint, steepness) if dynamic_weight else DANGER_ZONES_STANDARD_WEIGHT
    else:
        weight = danger_zones_heuristics_weight_function(placed_pieces) if dynamic_weight else DANGER_ZONES_STANDARD_WEIGHT

    player_danger = evaluate_danger_zones(player, opponent)
    opponent_danger = evaluate_danger_zones(opponent, player)
    denom = abs(player_danger) + abs(opponent_danger)
    if denom == 0:
        return 0
    combined_danger = weight * ((player_danger - opponent_danger) / denom)
    return combined_danger
