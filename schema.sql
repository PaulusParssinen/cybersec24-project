DROP TABLE IF EXISTS user_groups;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS boards;
DROP TABLE IF EXISTS threads;
DROP TABLE IF EXISTS posts;

CREATE TABLE user_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rank INTEGER DEFAULT 0,
    name TEXT NOT NULL
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_group_id INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (user_group_id) REFERENCES user_groups(id)
);

CREATE TABLE boards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    min_user_rank INTEGER DEFAULT 0
);

CREATE TABLE threads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    board_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content_body TEXT NOT NULL,
    FOREIGN KEY (board_id) REFERENCES boards(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    thread_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    content_body TEXT NOT NULL,
    FOREIGN KEY (thread_id) REFERENCES threads(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

INSERT INTO user_groups (rank, name) VALUES (0, 'Default');
INSERT INTO user_groups (rank, name) VALUES (5, 'Moderator');
INSERT INTO user_groups (rank, name) VALUES (10, 'Administrator');

INSERT INTO boards (name, description) VALUES ('General', 'This board is for general discussion.');

INSERT INTO users (username, password, user_group_id) VALUES ('Admin', 'pbkdf2:sha256:260000$Bht3OdPf60PRcoIe$b69fc6a93b7fc2b650acb4e0f5c50259eda51bc77b945a7217e22acd31271bae', 3); -- 'admin123'
INSERT INTO users (username, password, user_group_id) VALUES ('Demo', 'pbkdf2:sha256:260000$n8t5e2XxPiEdDgbA$c528be036bb260f8d8d78455f74f9be58a9bb3d8b6b16afc9dfa19dccccc639f', 1); -- 'demo123'