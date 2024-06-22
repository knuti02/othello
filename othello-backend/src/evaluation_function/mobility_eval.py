import math

def mobility_heuristics_weight_function(placed_pieces: int, maximum_weight: int = 50,  midpoint: int = 23, steepness: float = 0.3) -> float:
    return (-1*maximum_weight) / (1 + math.e ** (-1 * steepness * (placed_pieces - midpoint))) + maximum_weight

def mobility_eval(gamestate, player, opponent, placed_pieces, dynamic_weight = True):
    def get_mobility(player):
        player_valid_moves = bin(gamestate.get_valid_moves(player)).count('1')
        opponent_valid_moves = bin(gamestate.get_valid_moves(opponent)).count('1')
        all_valid_moves = player_valid_moves + opponent_valid_moves
        # Prevent division by zero
        if all_valid_moves == 0:
            return 0
        mobility = player_valid_moves / all_valid_moves
        return mobility
    
    weight = mobility_heuristics_weight_function(placed_pieces) if dynamic_weight else 5
    
    player_mobility = get_mobility(player)
    opponent_mobility = get_mobility(opponent)
    
    mobility_denominator = abs(player_mobility) + abs(opponent_mobility)
    # Prevent division by zero
    if mobility_denominator == 0:
        return 0
    
    combined_mobility = weight * ((player_mobility - opponent_mobility) / mobility_denominator)
    return combined_mobility