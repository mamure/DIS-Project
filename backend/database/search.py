from flask import Blueprint, render_template, request
from backend import conn
import re

Search = Blueprint("search", __name__)

def convertToPos(symbol : chr) -> int :
    """
    Converts a symbol from a pos e.g. 'c' from "c3d5" to integer 2 
    """
    if symbol.isdigit():
        return int(symbol)-1
    return ord(symbol) - ord('a')
    

def convertRawMoves(moves):
    """
    Function to convert a list of rotations to actual chess moves, eg. c5e3 -> Bc5xe3
    Moves are always returned on this form (without 'x' if no capture)
    """
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
        # Go through all moves and calculates which piece was moved and concatenates result to a string
        # Some moves are malformed (i.e. too long or too short), if that is the case,
        # the whole game is excluded from conversion
        if len(move) != 4:
            return ""
        
        (y0,x0,y1,x1) = (convertToPos(sym) for sym in list(move))
        # Loads the move i.e. c2c4 into a tuple
        
        # Set to ERROR if trying to move piece that does not exist on square
        # I might have missed chess rule, or the database might be wrongly typed
        piece = pos[x0][y0] or "ERROR"  
        capture = pos[x1][y1]
        x = "" if capture is None else "x"

        # Castling
        if piece == "K" and abs(y0 - y1) == 2:
            if pos[x1][y1+1] == "R":
                pos[x1][y1-1] = pos[x1][y1+1]
                pos[x1][y1+1] = None
            else:
                pos[x0][y1+1] = pos[x1][y1-2]
                pos[x1][y1-2] = None

        # En passant
        elif piece == "" and capture is None and abs(y0 - y1) == 1:
            pos[x1][y1 + 1 if y1 == 2 else y1 - 1] = None
        
        # Promotion (always assume queen because other cases are daunting)
        if piece == "" and y1 == 0 or y1 == 7:
            pos[x0][y0] = "Q"

        # Switch pos
        pos[x1][y1] = pos[x0][y0]
        pos[x0][y0] = None

        # Add to string-sequence of moves (to-be regex-matched later)
        seq += ''.join([piece, move[0:2], x, move[2:4], ", "])

    return seq

@Search.route('/search')
def search_games():

    query = request.args.get("query")
    query_name = request.args.get("name_query")
    white = request.args.get("playing_as")

    if not (query or query_name):
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
        """.format(white, query_name)
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
