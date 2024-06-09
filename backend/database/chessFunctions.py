from typing import List
from backend import conn
import pylcs


def createMovesID(moves0: str, moves1: str) -> List[str]:
    """
    Creates a unique symbol structure of the two move sequences so that moves are represented as a single symbol.
    The move-symbols are linked between the first and second move string.
    """
    used_chars = {}
    start_index = 33
    h_lst0 = []
    h_lst1 = []
    # Loops through all moves and adds a unique symbol to each unique move
    for move in moves0.split(", "):
        if move not in used_chars:
            used_chars[move] = chr(start_index)
            start_index += 1
        h_lst0.append(used_chars[move])
    # For the second move-string (using the same dictionar)
    for move in moves1.split(", "):
        if move not in used_chars:
            used_chars[move] = chr(start_index)
            start_index += 1
        h_lst1.append(used_chars[move])
    return h_lst0, h_lst1


def compareGames(moves0: str, moves1: str) -> float:
    """
    Compares two games that are converted by convertToPos to a string of moves seprated by commas.
    Returns a percentage of how similar the games are.
    """
    lst1, lst2 = createMovesID(moves0, moves1)
    max_length = max(len(lst1), len(lst2))
    seq1 = "".join(lst1)
    seq2 = "".join(lst2)
    return pylcs.lcs_sequence_length(seq1, seq2) / max_length


def convertToPos(symbol: chr) -> int:
    """
    Converts a symbol from a pos e.g. 'c' from "c3d5" to integer 2
    """
    if symbol.isdigit():
        return int(symbol) - 1
    return ord(symbol) - ord("a")


def convertRawMoves(moves: List[str]) -> str:
    """
    Function to convert a list of rotations to actual chess moves, eg. c5e3 -> Bc5xe3
    Moves are always returned on this form (without 'x' if no capture)
    """
    pos = [
        ["R", "N", "B", "Q", "K", "B", "N", "R"],
        ["", "", "", "", "", "", "", ""],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        ["", "", "", "", "", "", "", ""],
        ["R", "N", "B", "Q", "K", "B", "N", "R"],
    ]

    seq = ""

    for move in moves:
        # Go through all moves and calculates which piece was moved and concatenates result to a string
        # Some moves are malformed (i.e. too long or too short), if that is the case,
        # the whole game is excluded from conversion
        if len(move) != 4:
            return ""

        (y0, x0, y1, x1) = (convertToPos(sym) for sym in list(move))
        # Loads the move i.e. c2c4 into a tuple

        # Set to ERROR if trying to move piece that does not exist on square
        # I might have missed chess rule, or the database might be wrongly typed

        # Maybe just remove "ERROR"-case (assuming everything is well implemented and typed in database)
        piece = pos[x0][y0] if pos[x0][y0] != None else "ERROR"
        capture = pos[x1][y1]
        x = "" if capture is None else "x"

        # Castling
        if piece == "K" and abs(y0 - y1) == 2:
            if pos[x1][y1 + 1] == "R":
                pos[x1][y1 - 1] = pos[x1][y1 + 1]
                pos[x1][y1 + 1] = None
                seq += "O-O, "
            else:
                pos[x0][y1 + 1] = pos[x1][y1 - 2]
                pos[x1][y1 - 2] = None
                seq += "O-O-O, "
            pos[x1][y1] = pos[x0][y0]
            pos[x0][y0] = None
            continue

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
        seq += "".join([piece, move[0:2], x, move[2:4], ", "])

    return seq[0:-2]


def findMostSimilarGames(game_id: int) -> int:
    """
    Searches through the database and finds the most similar game to the provided game_id
    (excluding the game ID, of course).
    Returns the most similar game_id.
    Returns 0 if there are no games (besides game_id) or game_id does not exist in the database.
    """
    cur = conn.cursor()

    # Finds the game that is equal to game_id and compiles its moves
    cur.execute(
        f"""
        SELECT jsonb_build_object('moves', array_agg(moves ORDER BY move_num))
        FROM game_moves
        NATURAL JOIN move
        WHERE game_id = {game_id}
        """
    )

    # If there exists no such game, that is, Index is out of bounds, return 0
    if not q[0][0]['moves']:
        return 0

    comp_game = convertRawMoves(q[0][0]["moves"])

    # Finds all games not equal to ID
    cur.execute(
        f"""
        SELECT jsonb_build_object('game_id', game_id, 'moves', array_agg(moves ORDER BY move_num))
        FROM game_moves
        NATURAL JOIN move
        WHERE game_id <> {game_id}
        GROUP BY game_id;
        """
    )

    # Ugly for-loop to find most similar game in collection of games
    max_sim = 0
    index = None
    q = cur.fetchall()
    for i, move in enumerate(q):
        sim = compareGames(comp_game, convertRawMoves(move[0]["moves"]))
        if sim > max_sim:
            max_sim = sim
            index = i

    # If there exists more than one game, they will always be the most similar.
    # This is a precaution, if there is only one game in the database.
    return q[index][0]["game_id"] if index else 0


def get_full_game(game_id: int) -> dict:
    """
    Returns a dictionary with all the information about a game.
    """
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            to_jsonb(game)
            ||
            to_jsonb(event)
            ||
            jsonb_build_object(
                'moves',
                string_agg(
                    game_moves.move_num || '.' || move.moves,
                    ' '
                    ORDER BY game_moves.move_num
                ),
                'white_player',
                to_jsonb(wplayer),
                'black_player',
                to_jsonb(bplayer)
            )
        FROM game
        INNER JOIN game_played_at ON
            game.game_id = game_played_at.game_id
        INNER JOIN event ON
            game_played_at.event_name = event.event_name
        INNER JOIN white_player ON
            game.game_id = white_player.game_id
        INNER JOIN black_player ON
            game.game_id = black_player.game_id
        INNER JOIN player wplayer ON
            white_player.player_name = wplayer.player_name
        INNER JOIN player bplayer ON
            black_player.player_name = bplayer.player_name
        INNER JOIN game_moves ON game.game_id = game_moves.game_id
        INNER JOIN move ON game_moves.move_id = move.move_id
        WHERE game.game_id = %s
        GROUP BY game.game_id, event.*, bplayer.*, wplayer.*
        LIMIT 1
        """,
        (game_id,),
    )
    game = cur.fetchone()
    if not game:
        raise ValueError(f"Game with game_id {game_id} not found.")
    return game[0]
