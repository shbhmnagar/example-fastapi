CREATE TABLE votes(
    post_id INTEGER,
    user_id INTEGER,
    PRIMARY KEY (post_id,user_id),
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);