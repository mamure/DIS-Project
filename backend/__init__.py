from pathlib import Path
from flask import Flask
import psycopg2
import os

app = Flask(__name__, template_folder=Path(__file__).parent.parent.joinpath("web/templates"), static_folder=Path(__file__).parent.parent.joinpath("web/static"))

conn = psycopg2.connect(
    dbname="chess_db",
    host="localhost",
    port="5432",
    user=os.getenv("PG_USERNAME"),
    password=os.getenv("PG_PASSWORD")
)


from backend.database.index import Index
from backend.database.search import Search
from backend.database.upload import Upload

app.register_blueprint(Index)
app.register_blueprint(Search)
app.register_blueprint(Upload)
