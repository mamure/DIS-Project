import psycopg2

def create_database():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            host="localhost",
            port="5432"
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'chess_db'")
        exists = cur.fetchone()
        if not exists:
            cur.execute("CREATE DATABASE chess_db")
            print("Database 'chess_db' created successfully")
        else:
            print("Database 'chess_db' already exists")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL:", error)
    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")

def create_table():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname="chess_db",
            host="localhost",
            port="5432"
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id SERIAL PRIMARY KEY,
                event_name VARCHAR(100),
                site VARCHAR(100),
                event_date DATE,
                round VARCHAR(10),
                white_player VARCHAR(100),
                black_player VARCHAR(100),
                result VARCHAR(10),
                white_elo INTEGER,
                black_elo INTEGER,
                black_fide_id VARCHAR(20),
                white_fide_id VARCHAR(20),
                opening VARCHAR(100),
                variation VARCHAR(100),
                eco VARCHAR(10),
                moves TEXT
            )
        """)
        print("Table 'events' created successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL:", error)
    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")

if __name__ == "__main__":
    create_database()
    create_table()
