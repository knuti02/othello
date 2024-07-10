from .mobility_eval import mobility_eval
from .stability_eval import stability_eval
from .coin_eval import coin_eval
from .corners_eval import corners_eval
from .danger_zones_eval import danger_zones_eval
from .edges_eval import edges_eval
from .wedge_eval import wedge_eval

def combined_eval(gamestate, player, opponent_player, dynamic_weight = True, print_heuristics = False, beta_features = False):
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
    
    
    danger_zones = 0
    edges = 0
    wedges = 0
    if beta_features:  # Inclusion of beta features now surpass only the original features
        danger_zones = danger_zones_eval(gamestate, player, opponent_player)
        edges = edges_eval(gamestate, player, opponent_player) # edges surpasses only danger zones as beta feature
        wedges = wedge_eval(gamestate, player, opponent_player) # wedges surpasses only edges and danger zones as beta feature
        pass
    
    combined_heuristics = mobility + stability + coin + corners + danger_zones + edges + wedges
    
    if print_heuristics:
        print("Mobility: ", mobility)
        print("Stability: ", stability)
        print("Coin: ", coin)
        print("Corners: ", corners)

        if beta_features:
            print("Danger zones: ", danger_zones)
            print("Edges: ", edges)
            print("Wedges: ", wedges)
    
    return combined_heuristics