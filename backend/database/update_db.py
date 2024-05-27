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
        print("Succesfully connected to database before entering data")

        # Create a cursor object
        cur = conn.cursor()
        for entry in data:
            cur.execute("""
                INSERT INTO event (event_name, event_date, site)
                VALUES (%s, %s, %s)
                ON CONFLICT (event_name) DO NOTHING
            """, (
                entry['Event'],
                entry['Date'],
                entry['Site']
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
