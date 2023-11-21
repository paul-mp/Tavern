CREATE TABLE app_user (
    user_id  SERIAL,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS Characters(
    character_id SERIAL NOT NULL,
    username VARCHAR(255) NOT NULL,
    race VARCHAR(25) NOT NULL,
    class VARCHAR(25) NOT NULL,
    character_name VARCHAR(255) NOT NULL,
    strength_attribute int NOT NULL,
    dexterity_attribute int NOT NULL,
    constitution_attribute int NOT NULL,
    intelligence_attribute int NOT NULL,
    wisdom_attribute int NOT NULL,
    charisma_attribute int NOT NULL,
    character_level int NOT NULL,
    background VARCHAR(500) NOT NULL,
    PRIMARY KEY (character_id),
    FOREIGN KEY (username) REFERENCES Users(username)
);

CREATE TABLE IF NOT EXISTS Forum_posts(
    username VARCHAR(255) NOT NULL,
    post_id SERIAL NOT NULL, 
    discussion_post VARCHAR(255) NOT NULL,
    PRIMARY KEY (post_id),
    FOREIGN KEY (username) REFERENCES Users(username)
);

CREATE TABLE IF NOT EXISTS Forum_comments(
    username VARCHAR(255) NOT NULL,
    post_id SERIAL NOT NULL,
    discussion_comment VARCHAR(255) NOT NULL,
    PRIMARY KEY (post_id, username),
    FOREIGN KEY (username) REFERENCES Users(username),
    FOREIGN KEY (post_id) REFERENCES Forum_posts(post_id)
);