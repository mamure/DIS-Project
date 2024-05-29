DROP TABLE IF EXISTS game CASCADE;
CREATE TABLE game (
    game_id SERIAL PRIMARY KEY,
    result VARCHAR(7),
    game_date TEXT,
    eco CHAR(3)
);

DROP TABLE IF EXISTS player CASCADE;
CREATE TABLE player (
    player_name VARCHAR(255) PRIMARY KEY,
    elo INT,
    title VARCHAR(255),
    fide_id INT
);

DROP TABLE IF EXISTS event CASCADE;
CREATE TABLE event (
    event_name VARCHAR(255) PRIMARY KEY,
    event_date TEXT,
    site VARCHAR(255)
);

DROP TABLE IF EXISTS opening CASCADE;
CREATE TABLE opening (
    opening_name VARCHAR(255) PRIMARY KEY
);

DROP TABLE IF EXISTS variation CASCADE;
CREATE TABLE variation (
    variation_name VARCHAR(255) PRIMARY KEY,
    opening_name VARCHAR(255),
    FOREIGN KEY (opening_name) REFERENCES opening(opening_name)
);

DROP TABLE IF EXISTS move CASCADE;
CREATE TABLE move (
    move_id SERIAL PRIMARY KEY,
    moves TEXT
);

-- Relations
DROP TABLE IF EXISTS game_moves CASCADE;
CREATE TABLE game_moves (
    move_id SERIAL,
    game_id SERIAL,
    PRIMARY KEY (move_id, game_id),
    FOREIGN KEY (move_id) REFERENCES move(move_id),
    FOREIGN KEY (game_id) REFERENCES game(game_id)
);

DROP TABLE IF EXISTS opening_variation CASCADE;
CREATE TABLE opening_variation (
    opening_name VARCHAR(255),
    variation_name VARCHAR(255),
    PRIMARY KEY (opening_name, variation_name),
    FOREIGN KEY (opening_name) REFERENCES opening(opening_name),
    FOREIGN KEY (variation_name) REFERENCES variation(variation_name)
);

DROP TABLE IF EXISTS game_opening CASCADE;
CREATE TABLE game_opening (
    game_id SERIAL,
    opening_name VARCHAR(255),
    PRIMARY KEY (game_id, opening_name),
    FOREIGN KEY (game_id) REFERENCES game(game_id),
    FOREIGN KEY (opening_name) REFERENCES opening(opening_name)
);

DROP TABLE IF EXISTS white_player CASCADE;
CREATE TABLE white_player (
    game_id SERIAL,
    player_name VARCHAR(255),
    PRIMARY KEY (game_id, player_name),
    FOREIGN KEY (game_id) REFERENCES game(game_id),
    FOREIGN KEY (player_name) REFERENCES player(player_name)
);

DROP TABLE IF EXISTS black_player CASCADE;
CREATE TABLE black_player (
    game_id SERIAL,
    player_name VARCHAR(255),
    PRIMARY KEY (game_id, player_name),
    FOREIGN KEY (game_id) REFERENCES game(game_id),
    FOREIGN KEY (player_name) REFERENCES player(player_name)
);

DROP TABLE IF EXISTS game_played_at CASCADE;
CREATE TABLE game_played_at (
    game_id SERIAL,
    event_name VARCHAR(255),
    PRIMARY KEY (game_id, event_name),
    FOREIGN KEY (game_id) REFERENCES game(game_id),
    FOREIGN KEY (event_name) REFERENCES event(event_name)
);

DROP TABLE IF EXISTS opening_moves CASCADE;
CREATE TABLE opening_moves (
    move_id SERIAL,
    opening_name VARCHAR(255),
    PRIMARY KEY (move_id, opening_name),
    FOREIGN KEY (move_id) REFERENCES move(move_id),
    FOREIGN KEY (opening_name) REFERENCES opening(opening_name)
);