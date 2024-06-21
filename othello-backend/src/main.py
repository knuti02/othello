from evaluation_function.combined_eval import combined_eval
from othello.GameState import GameState
from AI_opponent.MinMaxAgent import MinMaxAgent
from gamestates.generate_gamestates import generate_gamestates
import time


def print_heuristics(game):
    print("\nCurrent evaluation: ")
    print("------------------------------------------------------------------------------")
    print("Black's current evaluation:", combined_eval(game, 'black', 'white', print_heuristics = True, beta_features = True))
    print("------------------------------------------------------------------------------")
    print("White's current evaluation:", combined_eval(game, 'white', 'black', print_heuristics = True, beta_features = True))
    print("------------------------------------------------------------------------------\n")

def do_move(game, move):
    if move == "skip":
        game.skip_turn()
    else:
        game.make_move(move[0], move[1])

def input_move(game):
    while True:
        move = input("\nEnter move (row+col): ")
        
        if move == "undo":
            game.undo_move()
            break
        elif move == "skip":
            game.skip_turn()
            break
        
        try:
            row=int(move[0])
            col=move[1].upper()
            valid_move = game.make_move(row, col)
            if valid_move:
                return
        except:
            print("Invalid move. Try again.")
            continue

def play_against_AI(game, player):
    agent = MinMaxAgent(cache={})
    print(game.board)

    while not game.game_over:
        if game.current_player == player:
            print("Your possible moves: ")
            print(game._bitboard_to_rowcol(game.get_valid_moves(player)))
            input_move(game)
            print(game.board)
            print_heuristics()
            continue
        
        _, move = agent.get_best_move(game, combined_eval, 5, beta_features=True)
        agent.clear_cache()
                
        print("AI move: ", move)
        if move == "skip":
            game.skip_turn()
        else:
            game.make_move(move[0], move[1])
        print(game.board)
        print_heuristics()
        

def play_AI_vs_AI(game, beta_features):
    start = time.time()
    print(game.board)
    agent = MinMaxAgent(cache={})  
    beta_features = beta_features
    
    while not game.game_over:
        # print("Current player:", game.current_player)
        # print("Current player's possible moves: ")
        # print(game._bitboard_to_rowcol(game.get_valid_moves(game.current_player)))
        _, move = agent.get_best_move(game, combined_eval, 5, beta_features=beta_features)
        agent.clear_cache()
        # print("AI move: ", move)
        if move == "skip":
            game.skip_turn()
        else:
            game.make_move(move[0], move[1])
        # print("Time taken: ", end - start)
        # print_heuristics(game)
        beta_features = not beta_features
    end = time.time()

    print("Game over!")
    print("Winner: ", game.winner)
    print("Time taken: ", end - start)
    return game.winner, not beta_features


def compare_ai(gamestates):
    new_win = 0
    old_win = 0
    tie = 0
    
    agent = MinMaxAgent(cache={})
    amount_of_games = len(gamestates)
    
    for i in range(amount_of_games):
        start = time.time()
        gamestate = GameState(gamestate = gamestates[i])
        print(gamestate.board)
        new_features = gamestate.current_player
        old_features = gamestate.target_player
        print("New features: ", new_features)
        print("Old features: ", old_features)
        
        while not gamestate.game_over:
            _, new_features_move = agent.get_best_move(gamestate, combined_eval, 5, beta_features=True)
            agent.clear_cache()
            do_move(gamestate, new_features_move)
            if gamestate.game_over:
                break
            
            _, old_features_move = agent.get_best_move(gamestate, combined_eval, 5, beta_features=False)
            agent.clear_cache()
            do_move(gamestate, old_features_move)

        if gamestate.winner == new_features:
            new_win += 1
        elif gamestate.winner == old_features:
            old_win += 1
        else:
            tie += 1
        
        end = time.time()
        print(f"Game {i+1} out of {amount_of_games}. \nTook {end - start} seconds. \nAll results: ")
        print("New features win: ", new_win)
        print("Old features win: ", old_win)
        print("Tie: ", tie, "\n")

        del gamestate
        
    print("Final results: ") 
    print("New features win: ", new_win)
    print("Old features win: ", old_win)
    print("Tie: ", tie)

if __name__ == "__main__":
    gamestates = generate_gamestates(100)
    print("Generated gamestates. Starting comparison... \n")
    compare_ai(gamestates)
    
    # play_AI_vs_AI(GameState(), beta_features = True)
        