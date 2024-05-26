#from heuristics.combined_heuristics import combined_heuristics
#from othello.BoardState import BoardState
#from othello.Color import Color
#from AI_opponent.MinMaxAgent import MinMaxAgent
from evaluation_function.combined_eval import combined_eval
from othello_revised.GameState import GameState
from AI_opponent.RevisedMinMaxAgent import MinMaxAgent
import time

def input_move(game):
    while True:
        move = input("\nEnter move (row+col): ")

        if move == "undo":
            game.undo_move()
            break
    

        if move == "skip":
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

    def print_heuristics():
        print("\nCurrent evaluation: ")
        print("------------------------------------------------------------------------------")
        print("Black's current evaluation:", combined_eval(game, 'black', 'white', print_heuristics = True, beta_features = True))
        print("------------------------------------------------------------------------------")
        print("White's current evaluation:", combined_eval(game, 'white', 'black', print_heuristics = True, beta_features = True))
        print("------------------------------------------------------------------------------\n")
    
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
        
# def play_against_player(game):
#     print(game.board)
#     opponent = Color.WHITE if game.current_player == Color.BLACK else Color.BLACK
    
#     while game.is_game_over() == False:
#         print("Current player:", game.current_player.name)
#         print("Current player's possible moves: ")
#         game.print_get_valid_moves(game.current_player)
        
#         input_move(game)
        
#         game.next_turn()
#         opponent = Color.WHITE if game.current_player == Color.BLACK else Color.BLACK
#         print("Move done!\n")
        
#         print("\nCurrent evaluation: ")
#         print("------------------------------------------------------------------------------")
#         print("Your (", game.current_player.name, ") current evaluation:", combined_heuristics(game, game.current_player))
#         print("------------------------------------------------------------------------------")
#         print("Your opponent's (", opponent.name, ") current evaluation:", combined_heuristics(game, opponent))
#         print("------------------------------------------------------------------------------")
        
#         print(game.board)
        

def play_AI_vs_AI(game, beta_features):
    print(game.board)
    agent = MinMaxAgent(cache={})  
    beta_features = beta_features
    
    while not game.game_over:
        print("Current player:", game.current_player)
        print("Current player's possible moves: ")
        print(game._bitboard_to_rowcol(game.get_valid_moves(game.current_player)))
        start = time.time()
        _, move = agent.get_best_move(game, combined_eval, 5, beta_features=beta_features)
        agent.clear_cache()
        print("AI move: ", move)
        if move == "skip":
            game.skip_turn()
        else:
            game.make_move(move[0], move[1])
        end = time.time()
        print("Time taken: ", end - start)
        print("\nCurrent evaluation: ")
        print("------------------------------------------------------------------------------")
        print("Black's current evaluation:", combined_eval(game, 'black', 'white', print_heuristics = True))
        print("------------------------------------------------------------------------------")
        print("White's current evaluation:", combined_eval(game, 'white', 'black', print_heuristics = True, beta_features = True))
        print("------------------------------------------------------------------------------\n")
        print(game.board)
        beta_features = not beta_features

    print("Game over!")
    print("Winner: ", game.winner)
    return game.winner, not beta_features

if __name__ == "__main__":
    game1 = GameState()
    game2 = GameState()
    winner1, using_beta_features1 = play_AI_vs_AI(game1, False)
    winner2, using_beta_features2 = play_AI_vs_AI(game2, True)
    
    print("Game 1 winner: ", winner1, ". Used beta features?: ", using_beta_features1)
    print("Game 2 winner: ", winner2, ". Used beta features?: ", using_beta_features2)
    
    # play_against_AI(game, 'black')
    
    # play_againt_AI = input("Do you want to play against the AI? (y/n): ")
    # if play_againt_AI == "ai_vs_ai":
    #     play_AI_vs_AI(game)
    
    # elif play_againt_AI == "y":
    #     play_againt_AI = True
    # else:
    #     play_againt_AI = False
    
    # if play_againt_AI:
    #     player = input("Do you want to play as black or white? (b/w): ")
    #     if player == "b":
    #         player = Color.BLACK
    #     elif player == "w":
    #         player = Color.WHITE
    #     else:
    #         print("Invalid input. Exiting...")
    #         exit() 
        
    #     play_against_AI(game, player)
    
    # else:
    #     play_against_player(game)
        
        