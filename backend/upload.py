from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import requests
import os
import chess.pgn
import io
from bs4 import BeautifulSoup
from update_db import update_database

app = Flask(__name__, template_folder='web/templates')

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files.get('upload_file')
    upload_url = request.form.get('upload_url')
    
    if uploaded_file:
        if uploaded_file.filename == '':
            return 'No file selected.'
        elif not uploaded_file.filename.endswith('.pgn'):
            return 'Invalid file format. Please upload a PGN file.'
        try:
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(file_path)
            data = parse_pgn_file(file_path)
            update_database(data)
            return 'Database updated successfully.'
        except Exception as e:
            print(f'An error occurred during update: {e}')
            return 'An error occurred during update.'
        
    elif upload_url:
        if not upload_url.startswith('https://www.pgnmentor.com/'):
            return 'Invalid URL.'
        try:
            data = parse_pgn_url(upload_url)
            update_database(data)
            return 'Database updated successfully.'
        except Exception as e:
            print(f'An error occurred during update: {e}')
            return 'An error occurred during update.'
    else:
        return 'Invalid request.'

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
        print(f"File '{file_path}' not found.")
    except IOError:
        print(f"Error reading file '{file_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return games

def parse_pgn_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        pgn_content = soup.find('pre').text.strip()
        
        pgn_io = io.StringIO(pgn_content)
        games = []
        while True:
            game = chess.pgn.read_game(pgn_io)
            if game is None:
                break
            game_data = extract_game_data(game)
            games.append(game_data)
        return games
    except requests.RequestException as e:
        raise ValueError(f"Error fetching PGN from URL: {e}")
    except Exception as e:
        raise ValueError(f"Error parsing PGN from URL: {e}")

def extract_game_data(game):
    return {
        'Event': game.headers.get('Event', 'No data'),
        'Site': game.headers.get('Site', 'No data'),
        'Date': game.headers.get('Date', 'No data'),
        'Round': game.headers.get('Round', 'No data'),
        'White': game.headers.get('White', 'No data'),
        'Black': game.headers.get('Black', 'No data'),
        'Result': game.headers.get('Result', 'No data'),
        'WhiteElo': game.headers.get('WhiteElo', 'No data'),
        'BlackElo': game.headers.get('BlackElo', 'No data'),
        'BlackFideId': game.headers.get('BlackFideId', 'No data'),
        'WhiteFideId': game.headers.get('WhiteFideId', 'No data'),
        'Opening': game.headers.get('Opening', 'No data'),
        'Variation': game.headers.get('Variation', 'No data'),
        'ECO': game.headers.get('ECO', 'No data'),
        'Moves': list(game.mainline_moves()),
    }

if __name__ == '__main__':
    app.run(debug=True)
