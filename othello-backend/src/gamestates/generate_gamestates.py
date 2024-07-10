import random
from evaluation_function.combined_eval import combined_eval
from othello.GameState import GameState

def generate_gamestates(n: int) -> list[(int, int, str)]:
    """
    Generate n random gamestates which are of roughly equal value
    Return a list where each index contains three tuples
    Each tuple contains the bitboard of black and white respectively, 
    and the last tuple contains the player to move ('black' or 'white')
    
    To my knowledge there are no good resoruces online for evaluating gamestates
    As such, we just use the combined evaluation function to evaluate positions
    In addition we dont store already generated gamestates as we want different ones
    """
    
    legal_games_generated = []
    while len(legal_games_generated) < n:
        number_of_moves = random.randint(4, 32) # early to mid game
        othello_game = GameState()
        
        for _ in range(number_of_moves):
            valid_moves = othello_game.get_valid_moves(othello_game.current_player)
            if valid_moves == 0:
                othello_game.skip_turn()
                continue
            
            move = random.choice(othello_game._bitboard_to_rowcol(valid_moves))
            othello_game.make_move(move[0], move[1])
        
        evaluation_black = combined_eval(othello_game, 'black', 'white', beta_features = True)
        evaluation_white = combined_eval(othello_game, 'white', 'black', beta_features = True)
        
        evaluation_difference = abs(evaluation_black - evaluation_white)
        game = (othello_game.board.get_board('black'), othello_game.board.get_board('white'), othello_game.current_player)
        if evaluation_difference < 5 and game not in legal_games_generated:
            legal_games_generated.append(game)
    
    return legal_games_generated    
    