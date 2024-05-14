CREATE TABLE IF NOT EXISTS game (
    game_id SERIAL PRIMARY KEY,
    result VARCHAR(7),
    game_date DATE,
    eco CHAR(3)
);

CREATE TABLE IF NOT EXISTS player (
    player_name VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255),
    elo INT,
    fide_id INT
);

CREATE TABLE IF NOT EXISTS event (
    event_name VARCHAR(255) PRIMARY KEY,
    event_date DATE,
    site VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS opening (
    opening_name VARCHAR(255) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS variation (
    variation_name VARCHAR(255) PRIMARY KEY,
    opening_name VARCHAR(255),
    FOREIGN KEY (opening_name) REFERENCES opening(opening_name)
);

CREATE TABLE IF NOT EXISTS move (
    move_id SERIAL PRIMARY KEY,
    moves TEXT
);

-- Relations
CREATE TABLE IF NOT EXISTS game_moves (
    move_id SERIAL,
    game_id SERIAL,
    PRIMARY KEY (move_id, game_id),
    FOREIGN KEY (move_id) REFERENCES move(move_id),
    FOREIGN KEY (game_id) REFERENCES game(game_id)
);

CREATE TABLE IF NOT EXISTS opening_variation (
    opening_name VARCHAR(255),
    variation_name VARCHAR(255),
    PRIMARY KEY (opening_name, variation_name),
    FOREIGN KEY (opening_name) REFERENCES opening(opening_name),
    FOREIGN KEY (variation_name) REFERENCES variation(variation_name)
);

CREATE TABLE IF NOT EXISTS game_opening (
    game_id SERIAL,
    opening_name VARCHAR(255),
    PRIMARY KEY (game_id, opening_name),
    FOREIGN KEY (game_id) REFERENCES game(game_id),
    FOREIGN KEY (opening_name) REFERENCES opening(opening_name)
);

CREATE TABLE IF NOT EXISTS white_player (
    game_id SERIAL,
    player_name VARCHAR(255),
    PRIMARY KEY (game_id, player_name),
    FOREIGN KEY (game_id) REFERENCES game(game_id),
    FOREIGN KEY (player_name) REFERENCES player(player_name)
);

CREATE TABLE IF NOT EXISTS black_player (
    game_id SERIAL,
    player_name VARCHAR(255),
    PRIMARY KEY (game_id, player_name),
    FOREIGN KEY (game_id) REFERENCES game(game_id),
    FOREIGN KEY (player_name) REFERENCES player(player_name)
);

CREATE TABLE IF NOT EXISTS game_played_at (
    game_id SERIAL,
    event_name VARCHAR(255),
    PRIMARY KEY (game_id, event_name),
    FOREIGN KEY (game_id) REFERENCES game(game_id),
    FOREIGN KEY (event_name) REFERENCES event(event_name)
);