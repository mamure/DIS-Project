from flask import Flask
from pathlib import Path

app = Flask(__name__, template_folder=Path(__file__).parent.parent.joinpath("web/templates"), static_folder=Path(__file__).parent.parent.joinpath("web/static"))
