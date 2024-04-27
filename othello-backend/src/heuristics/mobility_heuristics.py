import math

def mobility_heuristics_weight_function(placed_pieces: int, maximum_weight: int = 50,  midpoint: int = 23, steepness: float = 0.3) -> float:
    return (-1*maximum_weight) / (1 + math.e ** (-1 * steepness * (placed_pieces - midpoint))) + maximum_weight

def mobility_heuristics(gamestate, placed_pieces, current_squares, opponent_squares, dynamic_weight = True):
    def get_mobility(squares) -> int:
        mobility = 0
        current = squares[0].color
        opponent = opponent_squares[0].color
        
        current_valid_moves = gamestate.get_valid_moves(current)
        opponent_valid_moves = gamestate.get_valid_moves(opponent)
        
        if len(current_valid_moves) + len(opponent_valid_moves) == 0:
            print(gamestate.board)
        
        mobility = len(current_valid_moves) / (len(current_valid_moves) + len(opponent_valid_moves))
        return mobility
    
    weight = mobility_heuristics_weight_function(placed_pieces) if dynamic_weight else 5
    
    current_player_mobility = get_mobility(current_squares)
    opponent_mobility = get_mobility(opponent_squares)
    
    mobility_denominator = abs(current_player_mobility) + abs(opponent_mobility)
    if mobility_denominator == 0:
        return 0
    
    combined_mobility = weight * ((current_player_mobility - opponent_mobility) / (mobility_denominator))
    
    return combined_mobility