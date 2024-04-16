from heuristics.combined_heuristics import combined_heuristics
from othello.BoardState import BoardState
from othello.Color import Color

if __name__ == "__main__":
    game = BoardState()
    game.init()
    print(game.board)
    opponent = Color.WHITE if game.current_player == Color.BLACK else Color.BLACK

    
    while game.is_game_over() == False:
        print("Current player:", game.current_player.name)
        print("Current player's possible moves: ")
        game.print_get_valid_moves(game.current_player)
        

        # for debugging purposes
        print("\nOpponent player:", opponent.name)
        print("Opponent player's possible moves: ")
        game.print_get_valid_moves(opponent)
        
        while True:
            move = input("\nEnter move (row,col): ")

            if move == "!skip":
                game.skip_turn()
                break
            
            parts = move.split(",")
            row = int(parts[0].strip())
            col = int(parts[1].strip())
            
            valid_move = game.place_piece(row, col)
            if valid_move:
                break
        
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
        
        