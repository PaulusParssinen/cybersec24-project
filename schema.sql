CREATE TABLE user_groups (
    id SERIAL PRIMARY KEY,
    rank INTEGER DEFAULT 0,
    name TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    user_group_id INTEGER REFERENCES user_groups
);

CREATE TABLE boards (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    min_user_rank INTEGER DEFAULT 0
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    board_id INTEGER REFERENCES boards,
    user_id INTEGER REFERENCES users,
    created_at TIMESTAMP,
    title TEXT,
    content_body TEXT
);
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    thread_id INTEGER REFERENCES threads,
    user_id INTEGER REFERENCES users,
    created_at TIMESTAMP,
    content_body TEXT
);


/* TODO: Decision whether to have a starter post or have it inlined in the thread table */
/* TODO: Proper constraints, cascading deletion etc. */
/* TODO: Seed user groups */
/* TODO: Indexes */