from flask import Blueprint, render_template, request
from backend import conn
import re

Search = Blueprint("search", __name__)

def convertToPos(symbol):
    if symbol.isdigit():
        return int(symbol)-1
    return ord(symbol) - ord('a')
    

def convertRawMoves(moves):
    # Function to convert a list of rotations to actual chess moves, eg. c5e3 -> Bc5xe3
    # Moves are always returned on this form (without 'x' if no capture)

    pos = [["R","N","B","Q","K","B","N","R"],
           ["","","","","","","",""],
           [None,None,None,None,None,None,None,None],
           [None,None,None,None,None,None,None,None],
           [None,None,None,None,None,None,None,None],
           [None,None,None,None,None,None,None,None],
           ["","","","","","","",""],
           ["R","N","B","Q","K","B","N","R"]]

    seq = ""

    for move in moves:
        if len(move) != 4:
            return ""
        (a,b,c,d) = (convertToPos(sym) for sym in list(move))
        # Set to ERROR if trying to move piece that does not exist on square
        # I might have missed chess rule, or the database might be wrongly typed
        piece = "ERROR" if pos[b][a] is None else pos[b][a]
        capture = pos[d][c]
        x = "" if capture is None else "x"

        # Castling
        if piece == "K" and abs(a - c) == 2:
            if pos[d][c+1] == "R":
                pos[d][c-1] = pos[d][c+1]
                pos[d][c+1] = None
            else:
                pos[b][c+1] = pos[d][c-2]
                pos[d][c-2] = None

        # En passant
        elif piece == "" and capture is None and abs(a - c) == 1:
            c_ = c + 1 if c == 2 else c - 1 
            pos[d][c_] = None
        
        # Switch pos
        pos[d][c] = pos[b][a]
        pos[b][a] = None

        # Add to string-sequence of moves (to-be regex-matched later)
        seq += ''.join([piece, move[0:2], x, move[2:4], ", "])

    return seq

@Search.route('/search')
def search_games():

    query = request.args.get("query")
    query_name = request.args.get("name_query")
    isWhite = request.args.get("playing_as")

    if query is None or (query == "" and query_name == ""):
        return render_template("search.html")

    print(f"Searching for {query}")

    cur = conn.cursor()
    cur.execute("""
        SELECT jsonb_build_object('game_id', game_id, 'result', result, 'moves', array_agg(moves ORDER BY move_num))
        FROM player AS P
        NATURAL JOIN {0}_player
        NATURAL JOIN game_moves
        NATURAL JOIN move
        NATURAL JOIN game
        WHERE P.player_name LIKE '%{1}%'
        GROUP BY game_id, result;
        """.format(isWhite, query_name)
        )

    lst = []
    pattern = re.compile(query)
    for row in cur.fetchall():
        if pattern.search(convertRawMoves(row[0]['moves'])) != None:
            lst.append(row[0])

    return lst

    # cur.execute(
    #     """
    #     SELECT
    #     to_jsonb(game)
    #     ||
    #     jsonb_build_object(
    #         'moves',
    #         array_agg(move.moves ORDER BY game_moves.move_num)
    #     )
    #     --jsonb_build_object(
    #     --    'black_player', jsonb_agg(to_jsonb(black_player)),
    #     --    'event', jsonb_agg(to_jsonb(event)),
    #     --    'game_moves', jsonb_agg(to_jsonb(game_moves)),
    #     --    'game_opening', jsonb_agg(to_jsonb(game_opening)),
    #     --    'game_played_at', jsonb_agg(to_jsonb(game_played_at)),
    #     --    'move', jsonb_agg(to_jsonb(move)),
    #     --    'opening', jsonb_agg(to_jsonb(opening)),
    #     --    'opening_moves', jsonb_agg(to_jsonb(opening_moves)),
    #     --    'opening_variation', jsonb_agg(to_jsonb(opening_variation)),
    #     --    'player', jsonb_agg(to_jsonb(player)),
    #     --    'variation', jsonb_agg(to_jsonb(variation)),
    #     --    'white_player', jsonb_agg(to_jsonb(white_player))
    #     --)
    #     FROM game
    #     INNER JOIN game_moves ON game.game_id = game_moves.game_id
    #     INNER JOIN move ON game_moves.move_id = move.move_id
    #     group by game.game_id
    #     """
    #     )
