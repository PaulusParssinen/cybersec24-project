DROP TABLE IF EXISTS user_groups CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS boards CASCADE;
DROP TABLE IF EXISTS threads CASCADE;
DROP TABLE IF EXISTS posts CASCADE;

CREATE TABLE user_groups (
    id SERIAL PRIMARY KEY,
    rank INTEGER DEFAULT 0,
    name TEXT NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT Now(),
    user_group_id INTEGER REFERENCES user_groups DEFAULT 1 NOT NULL
);

CREATE TABLE boards (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    min_user_rank INTEGER DEFAULT 0
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    board_id INTEGER REFERENCES boards,
    user_id INTEGER REFERENCES users,
    created_at TIMESTAMP DEFAULT Now(),
    title TEXT NOT NULL,
    content_body TEXT NOT NULL
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    thread_id INTEGER REFERENCES threads ON DELETE CASCADE,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT Now(),
    content_body TEXT NOT NULL
);

INSERT INTO user_groups (rank, name) VALUES (0, 'Default');
INSERT INTO user_groups (rank, name) VALUES (5, 'Moderator');
INSERT INTO user_groups (rank, name) VALUES (10, 'Administrator');

INSERT INTO boards (name, description) VALUES ('General', 'This board is for general discussion.');