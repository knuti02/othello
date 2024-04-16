import math

def stability_heuristics_weight_function(placed_pieces: int, maximum_weight: int = 50,  midpoint: int = 37, steepness: float = 0.15) -> float:
    return (-1*maximum_weight) / (1 + math.e ** (-1 * steepness * (placed_pieces - midpoint))) + maximum_weight

def stability_heuristics(placed_pieces, current_squares, opponent_squares, dynamic_weight = True) -> int:
    safe_weight = 1
    stable_weight = 0
    unstable_weight = -1
    
    def get_stability(squares) -> int:
        stability = 0
        for square in squares:
            # Safe
            if square.stability == 1:
                stability += safe_weight / len(squares)
                continue
            # Stable
            elif square.stability == 0:
                stability += stable_weight
                continue
            # Unstable
            stability += unstable_weight / len(squares)
        
        #print("Stability-value of color", squares[0].color.name, ": ", stability)
        return stability
    
    # Calculate weight using the defined weight function
    weight = stability_heuristics_weight_function(placed_pieces) if dynamic_weight else 25

    # Calculate stability for current player and opponent
    current_player_stability = get_stability(current_squares)
    opponent_stability = get_stability(opponent_squares)
    
    # Calculate combined stability using the weighted difference between current player's and opponent's stability
    combined_stability = weight * ((current_player_stability - opponent_stability) / (abs(current_player_stability) + abs(opponent_stability)))
    
    return combined_stability
