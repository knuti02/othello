from .mobility_heuristics import mobility_heuristics
from .corners_heuristics import corners_heuristics
from .coin_heuristics import coin_heuristics
from .stability_heuristics import stability_heuristics

from othello.Color import Color

def combined_heuristics(gamestate, player, dynamic_weight = True, print_heuristics = False) -> float:
    if gamestate.is_game_over():
        if gamestate.get_winner() == None:
            return 0
        
        return float('inf') if gamestate.get_winner() == player else float('-inf')
    
    # Determine opponent player
    opponent_player = Color.WHITE if player == Color.BLACK else Color.BLACK
    
    # Get current player's and opponent's squares and calculate remaining squares on the board 
    current_squares = gamestate.player_pieces_map[player]
    opponent_squares = gamestate.player_pieces_map[opponent_player]
    placed_pieces = len(current_squares) + len(opponent_squares)
    
    stability = stability_heuristics(placed_pieces, current_squares, opponent_squares, dynamic_weight)
    coin_parity = coin_heuristics(placed_pieces, current_squares, opponent_squares, dynamic_weight)
    corners = corners_heuristics(gamestate, placed_pieces, current_squares, opponent_squares, dynamic_weight)
    mobility = mobility_heuristics(gamestate, placed_pieces, current_squares, opponent_squares, dynamic_weight)
    
    # for debugging purposes, print the heuristics
    if print_heuristics:
        print("Stability: ", stability)
        print("Coin parity: ", coin_parity)
        print("Corners: ", corners)
        print("Mobility: ", mobility)
    
    combined_heuristics = stability + coin_parity + corners + mobility
    return combined_heuristics