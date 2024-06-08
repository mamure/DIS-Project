# DIS-Project
### E/R Model
![](er_model.jpg)
# How to compile web-app
## Requirements
Run the code below in your terminal to install the necessary modules to compile the web-app.

```
pip install -r requirements.txt
```

* Make sure that your Postgres Server is configurated as following and turned on:

  
| host      | port |
|-----------|------|
| localhost | 5432 |

Then you can initialize the database with (if `python3` does not work replace it with `python`)
```
python3 init.py
```
Then you can compile the web-app and start the database by running the command line:
```
python3 run.py
```

# Tutorial on Web-App
The web-app is built up by some underlying sites, each with different implementations and use cases within the web app.

## _Home_
The home site serves as the navigational hub for the other sites.

## _Search_
Here, it is possible to search the database for games using the name of a player and a sequence of moves in the given players game. Both search-requirements uses regex-mathing (for player-names: in `PostreSQL`; for sequence of moves, with Python module `re`). This means that it is possible to search through the database for all players, if no player-name is supplied, since the empty string regex-matches all player names in this context.

It is also possible to search for similar games to a given game ID using the second search button. This uses a LCS-solver module in Python to find how similar games are. A single game is returned (if the database has more than one game in the collection).

## _Upload_
Here you can upload your own chess games to the DIScover chess database. The app supports either Portable Game Notation files (.pgn) or a link to a file from the website [PGN Mentor](https://www.pgnmentor.com/files.html).

If you have a [chess.com](https://www.chess.com) account, you can download a PGN file from the website and upload your very own games to DIScover Chess!

## _About_
This site contains a small section with information about this project.
