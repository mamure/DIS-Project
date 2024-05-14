import psycopg2

def update_database(events):
    conn = None
    try:
        conn = psycopg2.connect(
            dbname="chess_db",
            host="localhost",
            port="5432"
        )

        # Create a cursor object
        cur = conn.cursor()
        for event in events:
            cur.execute("""
                INSERT INTO events (event_name, site, event_date, round, white_player, black_player, result, white_elo, black_elo, black_fide_id, white_fide_id, opening, variation, eco, moves)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                event['Event'],
                event['Site'],
                event['Date'],
                event['Round'],
                event['White'],
                event['Black'],
                event['Result'],
                event['WhiteElo'],
                event['BlackElo'],
                event['BlackFideId'],
                event['WhiteFideId'],
                event['Opening'],
                event['Variation'],
                event['ECO'],
                ','.join(str(move) for move in event['Moves'])  # Convert moves list to string
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

if __name__ == "__main__":
    sample_event_data = [
        {
            'Event': 'Test Event',
            'Site': 'Test Site',
            'Date': '2024-05-12',
            'Round': '1',
            'White': 'Player 1',
            'Black': 'Player 2',
            'Result': '1-0',
            'WhiteElo': '2800',
            'BlackElo': '2600',
            'BlackFideId': '123456',
            'WhiteFideId': '654321',
            'Opening': 'Italian Game',
            'Variation': 'Giuoco Piano',
            'ECO': 'C50',
            'Moves': ['e4', 'e5', 'Nf3', 'Nc6', 'Bc4']
        }
    ]
    update_database(sample_event_data)