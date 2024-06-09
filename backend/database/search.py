from flask import Blueprint, render_template, request
from backend import conn
from backend.database.chessFunctions import convertRawMoves
from backend.database.chessFunctions import findMostSimilarGames, get_full_game
import re

Search = Blueprint("search", __name__)


@Search.route("/search")
def search_games():
    query = request.args.get("query")
    query_name = request.args.get("name_query")
    color = "white" if request.args.get("playing_as") == "white" else "black"
    game_id = request.args.get("game_id")

    cur = conn.cursor()

    if not (query or query_name or game_id):
        return render_template("search.html")

    # Searching for similar games in database based in game_id.
    # Maybe needs to be removed
    if game_id:
        if not isinstance(game_id, int):
            print(f"Game ID '{game_id}' is malformed (must be integer)")
            return render_template("search.html")

        most_similar = findMostSimilarGames(game_id)
        if most_similar:
            return render_template(
                "stats.html",
                stats1=get_full_game(game_id),
                stats2=get_full_game(most_similar),
                gid1=game_id,
                gid2=most_similar,
            )
        else:
            print(f"Game ID '{game_id}' not found in database")
            return render_template("search.html")

    print(f"Searching for {query}")

    # Finds all games where query_name matches player name of that color
    cur.execute(
        f"""
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

    # Regex-matches the sequence of moves to the games found of that player ID
    lst = []
    pattern = re.compile(query)
    for row in cur.fetchall():
        move_string = convertRawMoves(row[0]["moves"])
        if pattern.search(move_string) != None:
            row[0]["moves"] = move_string
            lst.append(row[0])

    return lst
