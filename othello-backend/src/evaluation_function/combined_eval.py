from .mobility_eval import mobility_eval
from .stability_eval import stability_eval
from .coins_eval import coins_eval
from .corners_eval import corners_eval
from .danger_zones_eval import danger_zones_eval
from .edges_eval import edges_eval
from .wedges_eval import wedges_eval
from .constants import *

def combined_eval(
        gamestate, player, opponent_player, 
        dynamic_weight=True, print_heuristics=False, heuristic_weight=None,
        mobility_hyperparameters = None, stability_hyperparameters = None, 
        coins_hyperparameters = None, corners_hyperparameters = None, danger_zones_hyperparameters = None, 
        edges_hyperparameters = None, wedges_hyperparameters = None, return_heuristics = False
    ):
    
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
    
    mobility = heuristic_weight.get('mobility', COMBINED_MOBILITY_WEIGHT) * mobility_eval(gamestate, player, opponent_player, placed_pieces, dynamic_weight, mobility_hyperparameters)
    stability = heuristic_weight.get('stability', COMBINED_STABILITY_WEIGHT) * stability_eval(gamestate, player, opponent_player, placed_pieces, dynamic_weight, stability_hyperparameters)
    coins = heuristic_weight.get('coins', COMBINED_COINS_WEIGHT) * coins_eval(gamestate, player, opponent_player, placed_pieces, dynamic_weight, coins_hyperparameters)
    corners = heuristic_weight.get('corners', COMBINED_CORNERS_WEIGHT) * corners_eval(gamestate, player, opponent_player, placed_pieces, dynamic_weight, corners_hyperparameters)
    danger_zones = heuristic_weight.get('danger_zones', COMBINED_DANGER_ZONES_WEIGHT) * danger_zones_eval(gamestate, player, opponent_player, placed_pieces, dynamic_weight, danger_zones_hyperparameters)
    edges = heuristic_weight.get('edges', COMBINED_EDGES_WEIGHT) * edges_eval(gamestate, player, opponent_player, placed_pieces, dynamic_weight, edges_hyperparameters)
    wedges = heuristic_weight.get('wedges', COMBINED_WEDGES_WEIGHT) * wedges_eval(gamestate, player, opponent_player, placed_pieces, dynamic_weight, wedges_hyperparameters)
    
    combined_heuristics = mobility + stability + coins + corners + danger_zones + edges + wedges
    
    if print_heuristics:
        print("Mobility: ", mobility)
        print("Stability: ", stability)
        print("Coin: ", coins)
        print("Corners: ", corners)
        print("Danger zones: ", danger_zones)
        print("Edges: ", edges)
        print("Wedges: ", wedges)
    
    # For analysis purposes
    if return_heuristics:
        return {
            'combined' : combined_heuristics,
            'mobility' : mobility,
            'stability' : stability,
            'coins' : coins,
            'corners' : corners,
            'danger_zones' : danger_zones,
            'edges' : edges,
            'wedges' : wedges
        }
    
    return combined_heuristics