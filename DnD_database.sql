CREATE TABLE app_user (
    user_id  SERIAL,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    vip boolean NOT NULL,
    battle_scars INTEGER NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS Characters(
    character_id SERIAL NOT NULL,
    username VARCHAR(255) NOT NULL,
    race VARCHAR(25) NOT NULL,
    class VARCHAR(25) NOT NULL,
    character_name VARCHAR(255) NOT NULL,
    background VARCHAR(500) NOT NULL,
    PRIMARY KEY (character_id),
    FOREIGN KEY (username) REFERENCES app_user(username)
);

CREATE TABLE IF NOT EXISTS Forum_posts(
    username VARCHAR(255) NOT NULL,
    post_id SERIAL NOT NULL, 
    discussion_post VARCHAR(255) NOT NULL,
    PRIMARY KEY (post_id),
    FOREIGN KEY (username) REFERENCES app_user(username)
);

CREATE TABLE IF NOT EXISTS Forum_comments(
    username VARCHAR(255) NOT NULL,
    post_id SERIAL NOT NULL,
    discussion_comment VARCHAR(255) NOT NULL,
    PRIMARY KEY (post_id, username),
    FOREIGN KEY (username) REFERENCES app_user(username),
    FOREIGN KEY (post_id) REFERENCES Forum_posts(post_id)
);