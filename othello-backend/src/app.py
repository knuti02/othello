from flask import Flask, request, jsonify
import sqlite3
from othello.GameState import GameState

app = Flask(__name__)
DATABASE = 'src/othello.db'
gamestate_store = {}

@app.before_first_request
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS games (
                  id INTEGER PRIMARY KEY, 
                  black_board INTEGER,
                  white_board INTEGER,
                  current_player TEXT,
                  current_turn INTEGER,
                  game_over BOOLEAN
            )'''
        )
    c.execute('''
              CREATE TABLE IF NOT EXISTS game_history (
                  game_id INTEGER,
                  turn INTEGER,
                  black_board INTEGER,
                  white_board INTEGER,
                  current_player TEXT,
                  PRIMARY KEY (game_id, turn)
              )'''
        )
    conn.commit()
    conn.close()

def save_gamestate(game_id, game_state):
    conn = sqlite3.connect('othello.db')
    c = conn.cursor()
    c.execute('REPLACE INTO games (id, black_board, white_board, current_player, current_turn, game_over) VALUES (?, ?, ?, ?, ?, ?)', 
              (game_id, game_state.black_board, game_state.white_board, game_state.current_player, game_state.current_turn, game_state.game_over))
    conn.commit()
    conn.close()

def save_game_history(game_id, game_state):
    conn = sqlite3.connect('othello.db')
    c = conn.cursor()
    c.execute('INSERT INTO game_history (game_id, turn, black_board, white_board, current_player) VALUES (?, ?, ?, ?, ?)', 
              (game_id, game_state.current_turn, game_state.black_board, game_state.white_board, game_state.current_player))
    conn.commit()
    conn.close()

def load_gamestate(game_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT black_board, white_board, current_player, current_turn, game_over FROM games WHERE id = ?', (game_id,))
    gamestate_information = c.fetchone()
    conn.close()
    
    if gamestate_information:
        return GameState(gamestate_information)
    return None

def load_game_history(game_id):
    conn = sqlite3.connect('othello.db')
    c = conn.cursor()
    c.execute('SELECT turn, black_board, white_board, current_player FROM game_history WHERE game_id = ? ORDER BY turn', (game_id,))
    rows = c.fetchall()
    conn.close()
    history = [{'turn': row[0], 'black_board': row[1], 'white_board': row[2], 'current_player': row[3]} for row in rows]
    return history

@app.route('/init', methods=['POST'])
def init():
    game_id = request.json.get('game_id', 1)
    gamestate = GameState()
    gamestate_store[game_id] = gamestate
    save_gamestate(gamestate)
    save_game_history(game_id, gamestate)
    return jsonify({
        'black_board': gamestate.board.get_board('black'),
        'white_board': gamestate.board.get_board('white'),
        'current_player': gamestate.current_player,
        'game_over': gamestate.game_over,
        'current_turn': gamestate.current_turn
    })    
    
@app.route('/get_gamestate', methods=['GET'])
def get_gamestate():
    game_id = request.args.get('game_id', 1)
    if game_id in gamestate_store:
        gamestate = gamestate_store[game_id]
    else:
        gamestate = load_gamestate(game_id)
        if gamestate:
            gamestate_store[game_id] = gamestate
        else:
            return jsonify({'error': 'Game not found'})
        
    return jsonify({
        'black_board': gamestate.board.get_board('black'),
        'white_board': gamestate.board.get_board('white'),
        'current_player': gamestate.current_player,
        'game_over': gamestate.game_over,
        'current_turn': gamestate.current_turn
    })
    
@app.route('/get_game_history', methods=['GET'])
def get_game_history():
    game_id = request.args.get('game_id', 1)
    history = load_game_history(game_id)
    return jsonify(history)

@app.route('/make_move', methods=['POST'])
def make_move():
    game_id = request.json.get('game_id', 1)
    row = request.json.get('row')
    col = request.json.get('col')
    
    if game_id in gamestate_store:
        gamestate = gamestate_store[game_id]
    else:
        gamestate = load_gamestate(game_id)
        if gamestate:
            gamestate_store[game_id] = gamestate
        else:
            return jsonify({'error': 'Game not found'})
        
    valid_move = gamestate.make_move(row, col)
    if not valid_move:
        return jsonify({'error': 'Invalid move'})
    
    save_gamestate(game_id, gamestate)
    save_game_history(game_id, gamestate)
    
    return jsonify({
        'black_board': gamestate.board.get_board('black'),
        'white_board': gamestate.board.get_board('white'),
        'current_player': gamestate.current_player,
        'game_over': gamestate.game_over,
        'current_turn': gamestate.current_turn
    })

@app.route('/')
def home():
    return 'Othello API'

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)