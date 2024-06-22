import math

def stability_heuristics_weight_function(placed_pieces: int, maximum_weight: int = 50,  midpoint: int = 37, steepness: float = 0.15) -> float:
    return (-1*maximum_weight) / (1 + math.e ** (-1 * steepness * (placed_pieces - midpoint))) + maximum_weight

def stability_eval(gamestate, player, opponent, placed_pieces, dynamic_weight = True):
    safe_weight = 1
    stable_weight = 0
    unstable_weight = -1
    
    def get_stability(player) -> int:
        player_board = gamestate.board.get_board(player)
        number_of_player_pieces = bin(player_board).count('1')
        safe_board = gamestate.board.safe_board[player]
        unstable_board = gamestate.board.unstable_board[player]
        stable_board = player_board & ~(safe_board | unstable_board)
        
        stability = (
            (bin(safe_board).count('1') * safe_weight) / number_of_player_pieces + 
            bin(stable_board).count('1') * stable_weight + 
            bin(unstable_board).count('1') * unstable_weight / number_of_player_pieces
        )
        
        # print(player)
        # print(f"safe: {bin(safe_board).count('1')}")
        # print(f"stable: {bin(stable_board).count('1')}")
        # print(f"unstable: {bin(unstable_board).count('1')}")
        
        return stability
    
    # Calculate weight using the defined weight function
    weight = stability_heuristics_weight_function(placed_pieces) if dynamic_weight else 25
    
    player_stability = get_stability(player)
    opponent_stability = get_stability(opponent)
    
    stability_denominator = abs(player_stability) + abs(opponent_stability)
    # prevent division by zero
    if stability_denominator == 0:
        return 0
    
    # Calculate combined stability using the weighted difference between current player's and opponent's stability
    combined_stability = weight * ((player_stability - opponent_stability) / stability_denominator)
    return combined_stability