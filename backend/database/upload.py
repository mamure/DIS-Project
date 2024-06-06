from flask import Blueprint, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
import requests
import os
import chess.pgn
import io
from backend.database.update_db import update_database

Upload = Blueprint("upload", __name__)

@Upload.route('/upload')
def upload_form():
    return render_template("upload.html")

@Upload.route("/upload", methods=["POST"])
def handle_upload():
    uploaded_file = request.files.get("upload_file")
    upload_url = request.form.get("upload_url")
    
    if uploaded_file:
        if uploaded_file.filename == "":
            flash("No file selected.", "error")
            return redirect(url_for("upload.upload_form"))
        elif not uploaded_file.filename.endswith(".pgn"):
            flash("Invalid file format. Please upload a PGN file.", "error")
            return redirect(url_for("upload.upload_form"))
        try:
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(Upload.config["UPLOAD_FOLDER"], filename)
            uploaded_file.save(file_path)
            parse_pgn_file(file_path)
            flash("Database updated successfully.", "success")
            return redirect(url_for("upload.upload_form"))
        except Exception as e:
            flash(f"An error occurred during update: {e}", "error")
            print(f"An error occurred during update: {e}")
            return redirect(url_for("upload.upload_form"))
        
    elif upload_url:
        if not upload_url.startswith("https://www.pgnmentor.com/"):
            flash("Invalid URL.", "error")
            return redirect(url_for("upload.upload_form"))
        try:
            parse_pgn_url(upload_url)
            flash("Database updated successfully.", "success")
            return redirect(url_for("upload.upload_form"))
        except Exception as e:
            flash(f"An error occurred during update: {e}", "error")
            print(f"An error occurred during update: {e}")
            return redirect(url_for("upload.upload_form"))
    else:
        flash("Invalid request.", "error")
        return redirect(url_for("upload.upload_form"))

def parse_pgn_file(file_path):
    games = []
    try:
        with open(file_path) as f:
            pgn = f.read()

        pgn_io = io.StringIO(pgn)
        while True:
            game = chess.pgn.read_game(pgn_io)
            if game is None:
                break
            game_data = extract_game_data(game)
            games.append(game_data)
    except FileNotFoundError:
        print(f'File "{file_path}" not found.')
    except IOError:
        print(f'Error reading file "{file_path}".')
    except Exception as e:
        print(f"An error occurred: {e}")
    update_database(games)

def parse_pgn_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        pgn_content = response.text.strip()
        
        pgn_io = io.StringIO(pgn_content)
        games = []
        while True:
            game = chess.pgn.read_game(pgn_io)
            if game is None:
                break
            game_data = extract_game_data(game)
            games.append(game_data)
        update_database(games)
    except requests.RequestException as e:
        raise ValueError(f"Error fetching PGN from URL: {e}")
    except Exception as e:
        raise ValueError(f"Error parsing PGN from URL: {e}")

def extract_game_data(game):
    moves = [move.uci() for move in game.mainline_moves()]
    return {
        "Event": game.headers.get("Event", "No data"),
        "Site": game.headers.get("Site", "No data"),
        "Date": game.headers.get("Date", "No data"),
        "Round": game.headers.get("Round", "No data"),
        "White": game.headers.get("White", "No data"),
        "Black": game.headers.get("Black", "No data"),
        "Result": game.headers.get("Result", "No data"),
        "WhiteElo": game.headers.get("WhiteElo", "0"),
        "BlackElo": game.headers.get("BlackElo", "0"),
        "BlackFideId": game.headers.get("BlackFideId", "0"),
        "WhiteFideId": game.headers.get("WhiteFideId", "0"),
        "WhiteTitle": game.headers.get("WhiteTitle", "No data"),
        "BlackTitle": game.headers.get("BlackTitle", "No data"),
        "Opening": game.headers.get("Opening", "No data"),
        "Variation": game.headers.get("Variation", "No data"),
        "ECO": game.headers.get("ECO", "No data"),
        "Moves": moves,
    }
