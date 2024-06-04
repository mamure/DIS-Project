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
    cur.execute(
        """
        SELECT
        to_jsonb(game)
        ||
        jsonb_build_object(
            'moves',
            array_agg(move.moves ORDER BY game_moves.move_num)
        )
        --jsonb_build_object(
        --    'black_player', jsonb_agg(to_jsonb(black_player)),
        --    'event', jsonb_agg(to_jsonb(event)),
        --    'game_moves', jsonb_agg(to_jsonb(game_moves)),
        --    'game_opening', jsonb_agg(to_jsonb(game_opening)),
        --    'game_played_at', jsonb_agg(to_jsonb(game_played_at)),
        --    'move', jsonb_agg(to_jsonb(move)),
        --    'opening', jsonb_agg(to_jsonb(opening)),
        --    'opening_moves', jsonb_agg(to_jsonb(opening_moves)),
        --    'opening_variation', jsonb_agg(to_jsonb(opening_variation)),
        --    'player', jsonb_agg(to_jsonb(player)),
        --    'variation', jsonb_agg(to_jsonb(variation)),
        --    'white_player', jsonb_agg(to_jsonb(white_player))
        --)
        FROM game
        INNER JOIN game_moves ON game.game_id = game_moves.game_id
        INNER JOIN move ON game_moves.move_id = move.move_id
        group by game.game_id
        """
    )
    return cur.fetchall()
    # for table in ["black_player","event","game","game_moves","game_opening","game_played_at","move","opening","opening_moves","opening_variation","player","variation","white_player"]:
    #     cur.execute(f"select * from {table}")
    #     res[table] = cur.fetchall()
    # return res
