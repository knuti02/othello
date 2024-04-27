from heuristics.combined_heuristics import combined_heuristics
from othello.BoardState import BoardState
from othello.Color import Color
from AI_opponent.MinMaxAgent import MinMaxAgent
import time

def input_move(game):
    while True:
        move = input("\nEnter move (row,col): ")

        if move == "skip":
            game.skip_turn()
            break
        
        parts = move.split(",")
        row = int(parts[0].strip())
        col = int(parts[1].strip())
        
        valid_move = game.place_piece(row, col)
        if valid_move:
            return

def play_against_AI(game, player):
    agent = MinMaxAgent(cache={})

    def print_heuristics():
        print("\nCurrent evaluation: ")
        print("------------------------------------------------------------------------------")
        print("Black's current evaluation:", combined_heuristics(game, Color.BLACK, print_heuristics = True))
        print("------------------------------------------------------------------------------")
        print("White's current evaluation:", combined_heuristics(game, Color.WHITE, print_heuristics = True))
        print("------------------------------------------------------------------------------\n")
    
    print(game.board)

    while game.is_game_over() == False:
        
        if game.current_player == player:
            print("Your possible moves: ")
            game.print_get_valid_moves(player)
            input_move(game)
            print(game.board)
            game.next_turn()
            print_heuristics()
            continue
        
        _, move = agent.get_best_move(game, combined_heuristics, 5)
        agent.clear_cache()
        
        # _, move = MinMaxAgent(game, combined_heuristics, 5, cache={})
        
        print("AI move: ", move)
        game.place_piece(move.row, move.col)
        print(game.board)
        game.next_turn()
        print_heuristics()
        
def play_against_player(game):
    print(game.board)
    opponent = Color.WHITE if game.current_player == Color.BLACK else Color.BLACK
    
    while game.is_game_over() == False:
        print("Current player:", game.current_player.name)
        print("Current player's possible moves: ")
        game.print_get_valid_moves(game.current_player)
        

        # for debugging purposes
        # print("\nOpponent player:", opponent.name)
        # print("Opponent player's possible moves: ")
        # game.print_get_valid_moves(opponent)
        
        input_move(game)
        
        
        game.next_turn()
        opponent = Color.WHITE if game.current_player == Color.BLACK else Color.BLACK
        print("Move done!\n")
        
        print("\nCurrent evaluation: ")
        print("------------------------------------------------------------------------------")
        print("Your (", game.current_player.name, ") current evaluation:", combined_heuristics(game, game.current_player))
        print("------------------------------------------------------------------------------")
        print("Your opponent's (", opponent.name, ") current evaluation:", combined_heuristics(game, opponent))
        print("------------------------------------------------------------------------------")
                
        print(game.board)

def play_AI_vs_AI(game):
    print(game.board)
    agent = MinMaxAgent(cache={})    
    
    while game.is_game_over() == False:
        print("Current player:", game.current_player.name)
        print("Current player's possible moves: ")
        game.print_get_valid_moves(game.current_player)
        
        start = time.time()
        _, move = agent.get_best_move(game, combined_heuristics, 5)
        end = time.time()
        print("AI move: ", move)
        print("Move took: ", end - start, " seconds")
        if move == "skip":
            game.skip_turn()
        else:
            game.place_piece(move.row, move.col)
        print(game.board)
        game.next_turn()
        print("Move done!\n")
        
        print("\nCurrent evaluation: ")
        print("------------------------------------------------------------------------------")
        print("Black's current evaluation:", combined_heuristics(game, Color.BLACK, print_heuristics = True))
        print("------------------------------------------------------------------------------")
        print("White's current evaluation:", combined_heuristics(game, Color.WHITE, print_heuristics = True))
        print("------------------------------------------------------------------------------\n")
    print("Game over!")
    print("Winner: ", game.get_winner().name)

if __name__ == "__main__":
    game = BoardState()
    game.init()

    
    play_againt_AI = input("Do you want to play against the AI? (y/n): ")
    if play_againt_AI == "ai_vs_ai":
        play_AI_vs_AI(game)
    
    elif play_againt_AI == "y":
        play_againt_AI = True
    else:
        play_againt_AI = False
    
    if play_againt_AI:
        player = input("Do you want to play as black or white? (b/w): ")
        if player == "b":
            player = Color.BLACK
        elif player == "w":
            player = Color.WHITE
        else:
            print("Invalid input. Exiting...")
            exit() 
        
        play_against_AI(game, player)
    
    else:
        play_against_player(game)
        
        