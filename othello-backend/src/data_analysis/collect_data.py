"""
Python script to run n amount of games where the models use slightly different heuristics
The purpose of this script is to evaluate the performance of the models

Will save into a star schema database where the fact table contains the game results
and the dimension tables contain the gamestates, moves and the models used
"""

import sqlite3
import numpy as np
import itertools
from functools import partial
from ..othello.GameState import GameState
from ..AI_opponent.MinMaxAgent import MinMaxAgent
from ..evaluation_function.combined_eval import combined_eval
from ..evaluation_function.constants import *
from .run_othello_ai_vs_ai import run_game

###########################
# Database helper methods #
###########################

def connect_db(db_name="othello_star_schema.db"):
    return sqlite3.connect(db_name)

def insert_model(conn, depth, heuristics):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO DimModel (Depth, MobilityWeight, StabilityWeight, CoinWeight, 
                              CornersWeight, DangerZonesWeight, EdgesWeight, WedgesWeight)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        depth,
        heuristics.get('mobility', COMBINED_MOBILITY_WEIGHT), 
        heuristics.get('stability', COMBINED_STABILITY_WEIGHT), 
        heuristics.get('coins', COMBINED_COINS_WEIGHT),
        heuristics.get('corners', COMBINED_CORNERS_WEIGHT), 
        heuristics.get('danger_zones', COMBINED_DANGER_ZONES_WEIGHT), 
        heuristics.get('edges', COMBINED_EDGES_WEIGHT),
        heuristics.get('wedges', COMBINED_WEDGES_WEIGHT)
    ))
    conn.commit()
    return cursor.lastrowid 

def insert_game_result(conn, game_id, black_model_id, white_model_id, final_score, winner):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO FactGame (GameID, BlackModelID, WhiteModelID, FinalScore, Winner)
        VALUES (?, ?, ?, ?, ?)
    ''', (game_id, black_model_id, white_model_id, final_score, winner))
    conn.commit()

def insert_game_state(conn, state):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO DimGameState (
            GameStateID, GameID, CurrentPlayer, MoveNumber, PiecesPlaced, CombinedScore,
            MobilityScore, StabilityScore, CoinsScore, CornersScore, DangerZonesScore,
            EdgesScore, WedgesScore, CurrentPlayerBitboard, OpponentBitboard
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        state['GameStateID'],
        state['GameID'],
        state['CurrentPlayer'],
        state['MoveNumber'],
        state['PiecesPlaced'],
        state['CombinedScore'],
        state['MobilityScore'],
        state['StabilityScore'],
        state['CoinsScore'],
        state['CornersScore'],
        state['DangerZonesScore'],
        state['EdgesScore'],
        state['WedgesScore'],
        state['CurrentPlayerBitboard'],
        state['OpponentBitboard']
    ))
    conn.commit()

def insert_move(conn, move):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO DimMoves (
            MoveID, GameID, MoveNumber, Player, Move
        ) VALUES (?, ?, ?, ?, ?)
    ''', (
        move['MoveID'],
        move['GameID'],
        move['MoveNumber'],
        move['Player'],
        move['Move']
    ))
    conn.commit()
    
    
def get_max_game_id(conn):
    """
    Get the highest GameID currently in the FactGame table.
    """
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(GameID) FROM FactGame')
    max_game_id = cursor.fetchone()[0]
    if max_game_id is None:
        return 0  # If no games have been inserted, start from 0
    return max_game_id

##############################
# Hyperparameter generators  #
##############################


def generate_weight_hyperparameters(heuristic_weight: dict, increments: int):
    """
    Generate weight hyperparameters for each heuristic in the dictionary.
    
    heuristic_weight: A dictionary where keys are heuristic names and values are default weights.
    increments: Number of values to generate between 0 and 1 (inclusive).
    
    Returns:
        A dictionary where each heuristic key maps to a list of evenly spaced weight values.
    """
    if increments < 2:
        raise ValueError("increments must be at least 2 to include 0 and 1.")
        
    weight_values = np.linspace(0, 1, increments).tolist()
    
    return {key: weight_values for key in heuristic_weight.keys()}


def generate_all_hyperparameter_combinations(weight_hyperparameters: dict):
    """
    Generate all possible combinations of hyperparameter values.
    
    weight_hyperparameters: A dictionary where keys are heuristic names and values are lists of possible values.
    
    Returns:
        A list of dictionaries, where each dictionary represents one possible combination of hyperparameter values.
    """
    keys = weight_hyperparameters.keys()
    values = weight_hyperparameters.values()

    # Create all possible combinations using itertools.product
    all_combinations = [
        dict(zip(keys, combination)) for combination in itertools.product(*values)
    ]
    
    return all_combinations

def generate_partial_evaluation_function(heuristics: dict):
    """
    Will generate a partial evaluation functions where specific heuristics 
    and hyperparameters are already decided. This way we only need to input gamestate and players
    """
        
    heuristic_weight_parameter = heuristics.get('heuristic_weight')
    mobility_hyperparameters_parameter = heuristics.get('mobility_hyperparameters')
    stability_hyperparameters_parameter = heuristics.get('stability_hyperparameters')
    coins_hyperparameters_parameter = heuristics.get('coins_hyperparameters')
    corners_hyperparameters_parameter = heuristics.get('corners_hyperparameters')
    danger_zones_hyperparameters_parameter = heuristics.get('danger_zones_hyperparameters')
    edges_hyperparameters_parameter = heuristics.get('edges_hyperparameters')
    wedges_hyperparameters_parameter = heuristics.get('wedges_hyperparameters')
    
    partial_evaluation_function = partial(
        combined_eval,
        dynamic_weight = True,
        print_heuristics = False,
        heuristic_weight = heuristic_weight_parameter,
        mobility_hyperparameters = mobility_hyperparameters_parameter,
        stability_hyperparameters = stability_hyperparameters_parameter,
        coins_hyperparameters = coins_hyperparameters_parameter,
        corners_hyperparameters = corners_hyperparameters_parameter,
        danger_zones_hyperparameters = danger_zones_hyperparameters_parameter,
        edges_hyperparameters = edges_hyperparameters_parameter,
        wedges_hyperparameters = wedges_hyperparameters_parameter
    )
    
    return partial_evaluation_function

def generate_dict_all_hyperparameters():
    return {
        'heuristic_weight' : None,
        'mobility_hyperparameters' : None,
        'stability_hyperparameters' : None,
        'coins_hyperparameters' : None,
        'corners_hyperparameters' : None,
        'danger_zones_hyperparameters' : None,
        'edges_hyperparameters' : None,
        'wedges_hyperparameters' : None
    }


#############################
# Data collection functions #
#############################

def collect_data_weight_hyperparameters(db_name="src/data_analysis/othello_star_schema.db"):
    conn = connect_db(db_name)
    game_id = get_max_game_id(conn)
    depth = 3
    # Standard model; should only be needed to be inserted once
    white_model_id = insert_model(conn, depth, {})
    
    weight_hyperparameters = generate_weight_hyperparameters(
        heuristic_weight = {
            'mobility' : 0, 'stability' : 0, 'coins' : 0, 'corners' : 0, 'danger_zones' : 0, 'edges' : 0, 'wedges' : 0
        }, increments = 3
    )
    combinations = generate_all_hyperparameter_combinations(weight_hyperparameters)
    
    for i in range(len(combinations)):
        # For the sake of clarity, these heuristics are used in the combined eval 
        # function as a flat weight for each of the smaller reward funcition
        heuristic_weight = combinations[i]
        game_id += 1
        game = GameState()
        model_one = MinMaxAgent(cache={})
        model_two = MinMaxAgent(cache={})
        
        black_model_id = insert_model(conn, depth, heuristic_weight)

        
        hyperparameters_dict = generate_dict_all_hyperparameters()
        hyperparameters_dict['heuristic_weight'] = heuristic_weight
        partial_evaluation_function = generate_partial_evaluation_function(hyperparameters_dict)
        evaluation_function_one = partial_evaluation_function
        evaluation_function_two = combined_eval
        
        result = run_game(game_id, game, model_one, model_two, evaluation_function_one, 
                          evaluation_function_two, search_depth = depth, combination = heuristic_weight)

        final_score = result['game_results']['FinalScore']
        winner = result['game_results']['Winner']
        insert_game_result(conn, game_id, black_model_id, white_model_id, final_score, winner)
        
        for state in result['game_states']:
            insert_game_state(conn, state)
        for move in result['moves']:
            insert_move(conn, move)

        print("Game " + str(game_id) + " done")
        
collect_data_weight_hyperparameters()