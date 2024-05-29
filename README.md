# DIS-Project
# Requirements
## Documentation
### E/R Model
![](er_model.jpg)

* Your database model (E/R diagram)
* How to compile your web-app from source (incl. scripts to initialize the database)?
* How to run and interact with your web-app?
## The web-app
* Should interact with the database via SQL (INSERT/UPDATE/DELETE/SELECT statements)
* [NEW] Should perform regular expression matching or context free grammar parsing
* Bonus points for use of views, triggers, stored procedures, but not required

# How to compile web-app
## Requirements
Run the code below in your terminal to install the necessary modules to compile the web-app.

```
$ pip install -r requirements.txt
```

* Make sure that your Postgres Server is configurated as following:
| host      | port |
|-----------|------|
| localhost | 5432 |

Then you can compile the web-app and start the database by running the command line:
```
$ python3 app.py
```

# Tutorial on Web-App
The web-app is built up by some underlying sites, each with different implementations and use cases within the web app.

## _Home_
The home site serves as the navigational hub for the other sites.

## _Database_
Here you can search in the database. The database contains entries from the start of the web-app that you can search through. Additionally, you can search after you have uploaded your games. You can search based on bla, bla, bla.

## _Upload_
Here you can upload your own chess games to the DIScover chess database. The app supports either Portable Game Notation files (.pgn) or a link to a file from the website [PGN Mentor](https://www.pgnmentor.com/files.html).

If you have a [chess.com](https://www.chess.com) account, you can download a PGN file from the website and upload your very own games to DIScover Chess!

## _About_
This site contains a small section with information about this project.
