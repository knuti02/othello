import math
from .constants import COINS_STANDARD_WEIGHT, COINS_DYNAMIC_MAX_WEIGHT, COINS_DYNAMIC_MIDPOINT, COINS_DYNAMIC_STEEPNESS

def coins_heuristics_weight_function(
        placed_pieces: int, 
        maximum_weight: int = COINS_DYNAMIC_MAX_WEIGHT,  
        midpoint: int = COINS_DYNAMIC_MIDPOINT, 
        steepness: float = COINS_DYNAMIC_STEEPNESS
    ) -> float:
    return (maximum_weight) / (1 + math.e ** (-1* steepness * (placed_pieces - midpoint)))

def coins_eval(gamestate, player, opponent, placed_pieces, dynamic_weight = True, coins_hyperparameters = None):
    """
    Evaluation function for coin parity: compares the number of coins for the player and opponent.
    """
    def get_coins_count(player) -> int:
        return bin(gamestate.board.get_board(player)).count('1')


    if coins_hyperparameters is not None:
        maximum_weight = coins_hyperparameters.get('maximum_weight', COINS_DYNAMIC_MAX_WEIGHT)
        midpoint = coins_hyperparameters.get('midpoint', COINS_DYNAMIC_MIDPOINT)
        steepness = coins_hyperparameters.get('steepness', COINS_DYNAMIC_STEEPNESS)
        weight = coins_heuristics_weight_function(placed_pieces, maximum_weight, midpoint, steepness) if dynamic_weight else COINS_STANDARD_WEIGHT
    else:
        weight = coins_heuristics_weight_function(placed_pieces) if dynamic_weight else COINS_STANDARD_WEIGHT

    current_player_coin_count = get_coins_count(player)
    opponent_coin_count = get_coins_count(opponent)

    combined_coin_parity = weight * ((current_player_coin_count - opponent_coin_count) / (abs(current_player_coin_count) + abs(opponent_coin_count)))

    return combined_coin_parity