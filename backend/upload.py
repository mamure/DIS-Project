from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import requests
import os

app = Flask(__name__, template_folder='/Users/martinreich1/Documents/KU/DIS/DIS-Project/web/templates')

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    upload_file = request.files.get('upload_file')
    upload_url = request.form.get('upload_url')
    
    if upload_file:
        if upload_file.filename == '':
            return 'No selected file'
        elif not upload_file.filename.endswith('.pgn'):
            return 'Invalid file format, please upload a PGN file'
        try:
            filename = secure_filename(upload_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            data = parse_pgn_file(file_path)
            update_database(data)
            return 'Database updated successfully'
        except:
            print("An error occurred during update")
        
    elif upload_url:
        if not upload_url.startswith('https://www.pgnmentor.com/'):
            return 'Invalid URL'
        try:
            response = requests.get(upload_url)
            if response.status_code == 200:
                data = parse_pgn_url(upload_url)
                update_database(data)
                return 'Database updated successfully'
            else:
                return 'Failed to fetch PGN from URL'
        except Exception as e:
            return str(e)
    else:
        return 'Invalid request'

def parse_pgn_file(file):
    print('Say Hi')
    pass
    
def parse_pgn_url(url):
    print('Say Hi (again)')
    pass

def update_database():
    print('Hi')
    pass

if __name__ == '__main__':
    app.run(debug=True)