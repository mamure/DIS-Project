import psycopg2
from flask import Flask, render_template
from pathlib import Path

app = Flask(__name__, template_folder='DIS-Project/web/templates')

def create_database():
    conn = None
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432"
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
            port="5432"
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

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    create_database()
    create_table()
    app.run(debug=True)