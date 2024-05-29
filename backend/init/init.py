import psycopg2
from pathlib import Path
from dotenv import load_dotenv
import os
from backend.init.initParse import main as init_parse_main
from backend.database.upload import parse_pgn_url

load_dotenv()

def create_database():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="postgres",
            user=os.getenv("PG_USERNAME"),
            password=os.getenv("PG_PASSWORD"),
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("DROP DATABASE IF EXISTS chess_db;")
        cur.execute("CREATE DATABASE chess_db;")
        print("Database 'chess_db' created successfully")

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
            port="5432",
            user=os.getenv("PG_USERNAME"),
            password=os.getenv("PG_PASSWORD"),
        )
        conn.autocommit = True
        cur = conn.cursor()
        initFile = Path(__file__).parent.joinpath("init.sql")
        cur.execute(initFile.open("r").read())
        print("Tables created successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL:", error)
    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")
            
def initDataUpload(data):
    for file in data:
        link = f"https://www.pgnmentor.com/{file}"
        parse_pgn_url(link)


def init_db():
    create_database()
    create_table()
    initLinks = init_parse_main()
    initDataUpload(initLinks)
