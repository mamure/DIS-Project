import tempfile
from flask import Blueprint, request, render_template, current_app
from markupsafe import Markup
import chess.pgn
import chess.svg
from backend import conn
from psycopg2._psycopg import cursor
import io

Svg = Blueprint("svg", __name__)

@Svg.route('/svg')
def svg_board():
    move_num = max(int(request.args.get("move_num", 1)), 1)
    game_id1 = request.args.get("game_id1")
    game_id2 = request.args.get("game_id2")
    is_white = int(request.args.get("is_white", 1)) != 0
    if not (game_id1 and game_id2):
        return "Both game_id1 and game_id2 needs to be given."
    cur = conn.cursor()
    game1, amnt_moves1 = get_game(game_id1, cur)
    game2, amnt_moves2 = get_game(game_id2, cur)
    equiv_move = False

    i = 1
    board1 = game1.board()
    move1 = None
    for move in game1.mainline_moves():
        if i >= move_num:
            break
        board1.push(move)
        i += 1
        move1 = move
    i = 1
    board2 = game2.board()
    move2 = None
    for move in game2.mainline_moves():
        if i >= move_num:
            break
        board2.push(move)
        i += 1
        move2 = move

    if move1 and move2:
        print(move1.uci(), move2.uci())
        equiv_move = move1.uci() == move2.uci()

    svg1 = chess.svg.board(
        board1,
        flipped=not is_white,
        lastmove=move1 if equiv_move else None,
        size=350,
    )
    svg2 = chess.svg.board(
        board2,
        flipped=not is_white,
        lastmove=move2 if equiv_move else None,
        size=350,
    )
    return render_template("svg_board.html", svg1=Markup(svg1),svg2=Markup(svg2), max_num=max(amnt_moves1, amnt_moves2), cur_num=move_num)


def get_game(game_id: int, cur: cursor):
    cur.execute("""
        SELECT
            to_jsonb(game)
            ||
            jsonb_build_object(
                'moves',
                array_agg(move.moves ORDER BY game_moves.move_num)
            )
        FROM game
        INNER JOIN game_moves ON game.game_id = game_moves.game_id
        INNER JOIN move ON game_moves.move_id = move.move_id
        WHERE game.game_id = %s
        group by game.game_id
        """,
        (game_id,)
        )
    game = cur.fetchone()
    if not game:
        raise ValueError(f"Game with game_id {game_id} not found.")
    return chess.pgn.read_game(io.StringIO(" ".join([f"{idx+1}.{m}" for idx, m in enumerate(game[0]["moves"])]))), len(game[0]["moves"])