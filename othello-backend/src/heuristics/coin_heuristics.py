import math

def coin_heuristics_weight_function(placed_pieces: int, maximum_weight: int = 95,  midpoint: int = 45, steepness: float = 0.9) -> float:
    return (maximum_weight) / (1 + math.e ** (-1* steepness * (placed_pieces - midpoint)))

def coin_heuristics(placed_pieces, current_squares, opponent_squares, dynamic_weight = True):
    def get_coin_parity(squares) -> int:
        coin_parity = len(squares)
        return coin_parity

    weight = coin_heuristics_weight_function(placed_pieces) if dynamic_weight else 25

    current_player_coin_parity = get_coin_parity(current_squares)
    opponent_coin_parity = get_coin_parity(opponent_squares)

    combined_coin_parity = weight * ((current_player_coin_parity - opponent_coin_parity) / (abs(current_player_coin_parity) + abs(opponent_coin_parity)))

    return combined_coin_parity