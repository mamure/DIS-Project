from backend import app
import os

if __name__ == "__main__":
    app.run(debug=bool(os.getenv("DEBUG", "false").capitalize()))
