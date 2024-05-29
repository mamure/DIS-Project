from flask import Blueprint, render_template, request
from backend import conn

Search = Blueprint("search", __name__)


@Search.route('/search')
def search_games():

    query = request.args.get("query")

    if query is None:
        return render_template("search.html")

    print(f"Searching for {query}")
    res = {}
    cur = conn.cursor()
    for table in ["black_player","event","game","game_moves","game_opening","game_played_at","move","opening","opening_moves","opening_variation","player","variation","white_player"]:
        cur.execute(f"select * from {table}")
        res[table] = cur.fetchall()
    return res
