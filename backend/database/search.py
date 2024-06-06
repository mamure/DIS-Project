from flask import Blueprint, render_template, request
from backend import conn
from numpy import argmax
from backend.database.chessFunctions import convertRawMoves
from backend.database.chessFunctions import findMostSimilarGames
import re

Search = Blueprint("search", __name__)

@Search.route('/search')
def search_games():

    query = request.args.get("query")
    query_name = request.args.get("name_query") 
    color = "white" if request.args.get("playing_as") == "white" else "black" 
    game_id  = request.args.get("game_id") 
    
    cur = conn.cursor()
    
    if not (query or query_name or game_id):
        return render_template("search.html")

    # Searching for similar games in database based in game_id.
    # Maybe needs to be removed
    if game_id:
        most_similar = findMostSimilarGames(game_id)
        if most_similar:
            cur.execute(f"""
                SELECT *
                FROM game
                WHERE game_id = '{most_similar}';
                """
                )
        else:
            return render_template("search.html")
        return cur.fetchall()

    print(f"Searching for {query}")

    # Finds all games where query_name matches player name of that color
    cur.execute(f"""
        SELECT jsonb_build_object('game_id', game_id, 'player_name', P.player_name, 'result', result, 'moves', array_agg(moves ORDER BY move_num))
        FROM player AS P
        NATURAL JOIN {color}_player
        NATURAL JOIN game_moves
        NATURAL JOIN move
        NATURAL JOIN game
        WHERE P.player_name LIKE '%{query_name}%'
        GROUP BY game_id, P.player_name, result;
        """
        )
    # ^^ Maybe use more complicated regex in postresql

    # Regex-matches the sequence of moves to the games found of that player ID
    lst = []
    pattern = re.compile(query)
    for row in cur.fetchall():
        move_string = convertRawMoves(row[0]['moves'])
        if pattern.search(move_string) != None:
            row[0]['moves'] = move_string
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
