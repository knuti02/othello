from .mobility_eval import mobility_eval
from .stability_eval import stability_eval
from .coins_eval import coins_eval
from .corners_eval import corners_eval
from .danger_zones_eval import danger_zones_eval
from .edges_eval import edges_eval
from .wedges_eval import wedges_eval

def combined_eval(gamestate, player, opponent_player, dynamic_weight=True, print_heuristics=False, heuristic_weight=None):
    if heuristic_weight is None:
        heuristic_weight = {
            'mobility': 1, 'stability': 1, 'coin': 1, 
            'corners': 1, 'danger_zones': 1, 'edges': 1, 'wedges': 1
        }
    
    if gamestate.game_over:
        if gamestate.winner == 'draw':
            return 0
        
        return float('inf') if gamestate.winner == player else float('-inf')
    
    player_board, opponent_board = gamestate.board.get_board(player), gamestate.board.get_board(opponent_player)
    placed_pieces = bin(player_board | opponent_board).count('1')
    
    mobility = heuristic_weight.get('mobility', 1) * mobility_eval(gamestate, player, opponent_player, placed_pieces, dynamic_weight)
    stability = heuristic_weight.get('stability', 1) * stability_eval(gamestate, player, opponent_player, placed_pieces, dynamic_weight)
    coins = heuristic_weight.get('coins', 1) * coins_eval(gamestate, player, opponent_player, placed_pieces, dynamic_weight)
    corners = heuristic_weight.get('corners', 1) * corners_eval(gamestate, player, opponent_player, placed_pieces, dynamic_weight)
    danger_zones = heuristic_weight.get('danger_zones', 1) * danger_zones_eval(gamestate, player, opponent_player, placed_pieces, dynamic_weight)
    edges = heuristic_weight.get('edges', 1) * edges_eval(gamestate, player, opponent_player, placed_pieces, dynamic_weight)
    wedges = heuristic_weight.get('wedges', 1) * wedges_eval(gamestate, player, opponent_player, placed_pieces, dynamic_weight)
    
    combined_heuristics = mobility + stability + coins + corners + danger_zones + edges + wedges
    
    if print_heuristics:
        print("Mobility: ", mobility)
        print("Stability: ", stability)
        print("Coin: ", coins)
        print("Corners: ", corners)
        print("Danger zones: ", danger_zones)
        print("Edges: ", edges)
        print("Wedges: ", wedges)
    
    return combined_heuristics