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

`$ pip install -r requirements.txt`

* Make sure that your Postgres Server is configurated as following:
| host      | port |
|-----------|------|
| localhost | 5432 |

# Tutorial on web-app