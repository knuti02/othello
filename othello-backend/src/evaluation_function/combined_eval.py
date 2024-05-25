from .mobility_eval import mobility_eval
from .stability_eval import stability_eval
from .coin_eval import coin_eval
from .corners_eval import corners_eval

def combined_eval(gamestate, player, opponent_player, dynamic_weight = True, print_heuristics = False):
    if gamestate.game_over:
        if gamestate.winner == 'draw':
            return 0
        
        return float('inf') if gamestate.winner == player else float('-inf')
    
    player_board = gamestate.board.get_board(player)
    opponent_player_board = gamestate.board.get_board(opponent_player)
    placed_pieces = bin(player_board | opponent_player_board).count('1')
    
    mobility = mobility_eval(gamestate, player, opponent_player, placed_pieces, dynamic_weight)
    stability = stability_eval(gamestate, player, opponent_player, placed_pieces, dynamic_weight)
    coin = coin_eval(gamestate, player, opponent_player, placed_pieces, dynamic_weight)
    corners = corners_eval(gamestate, player, opponent_player, placed_pieces, dynamic_weight)
    
    if print_heuristics:
        print("Mobility: ", mobility)
        print("Stability: ", stability)
        print("Coin: ", coin)
        print("Corners: ", corners)
        
    combined_heuristics = mobility + stability + coin + corners
    return combined_heuristics