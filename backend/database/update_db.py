import psycopg2
import os

def update_database(data):
    conn = None
    try:
        conn = psycopg2.connect(
            dbname="chess_db",
            host="localhost",
            port="5432",
            user=os.getenv("PG_USERNAME"),
            password=os.getenv("PG_PASSWORD")
        )
        print("Successfully connected to database before entering data")

        cur = conn.cursor()
        for entry in data:
            cur.execute("""
                INSERT INTO event (event_name, event_date, site)
                VALUES (%s, %s, %s)
                ON CONFLICT (event_name) DO NOTHING
                """, (
                entry["Event"],
                entry["Date"],
                entry["Site"]
            ))

            cur.execute("""
                INSERT INTO player (player_name, elo, title, fide_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (player_name) DO NOTHING
                """, (
                entry["White"],
                int(entry["WhiteElo"]) if entry["WhiteElo"].isdigit() else None,
                entry["WhiteTitle"],
                int(entry["WhiteFideId"]) if entry["WhiteFideId"].isdigit() else None
            ))

            cur.execute("""
                INSERT INTO player (player_name, elo, title, fide_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (player_name) DO NOTHING
                """, (
                entry["Black"],
                int(entry["BlackElo"]) if entry["BlackElo"].isdigit() else None,
                entry["BlackTitle"],
                int(entry["BlackFideId"]) if entry["BlackFideId"].isdigit() else None
            ))

            cur.execute("""
                INSERT INTO game (result, game_date, eco)
                VALUES (%s, %s, %s)
                RETURNING game_id
                """, (
                entry["Result"],
                entry["Date"],
                entry["ECO"]
            ))
            game_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO white_player (game_id, player_name)
                VALUES (%s, %s)
                """, (
                game_id,
                entry["White"]
            ))

            cur.execute("""
                INSERT INTO black_player (game_id, player_name)
                VALUES (%s, %s)
                """, (
                game_id,
                entry["Black"]
            ))

            move_ids = []
            for move in entry["Moves"]:
                cur.execute("""
                    INSERT INTO move (moves)
                    VALUES (%s)
                    RETURNING move_id
                    """, (move,))
                move_ids.append(cur.fetchone()[0])

            for idx, move_id in enumerate(move_ids):
                cur.execute("""
                    INSERT INTO game_moves (move_id, move_num, game_id)
                    VALUES (%s, %s, %s)
                    """, (
                    move_id,
                    idx + 1,
                    game_id
                ))

            cur.execute("""
                INSERT INTO opening (opening_name)
                VALUES (%s)
                ON CONFLICT (opening_name) DO NOTHING
                """, (
                    entry["Opening"],
                    ))

            cur.execute("""
                INSERT INTO variation (variation_name, opening_name)
                VALUES (%s, %s)
                ON CONFLICT (variation_name) DO NOTHING
                """, (
                    entry["Variation"], 
                    entry["Opening"]
                    ))

            cur.execute("""
                INSERT INTO game_opening (game_id, opening_name)
                VALUES (%s, %s)
                """, (
                game_id,
                entry["Opening"]
            ))

            cur.execute("""
                INSERT INTO game_played_at (game_id, event_name)
                VALUES (%s, %s)
                """, (
                game_id,
                entry["Event"]
            ))

        conn.commit()
        print("Records inserted successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")
