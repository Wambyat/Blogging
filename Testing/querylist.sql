CREATE TABLE user_info(id INTEGER PRIMARY KEY, name varchar(20), password varchar(30));
CREATE TABLE blog_info(bid INTEGER PRIMARY KEY, btitle varchar(20), uid varchar(30), bcontent TEXT, FOREIGN KEY (uid) REFERENCES user_info(id));
CREATE TABLE blog_like (blog_id INTEGER, user_id INTEGER, FOREIGN KEY(blog_id) REFERENCES blog(bid), FOREIGN KEY(user_id) REFERENCES user(id));
CREATE TABLE blog_fav (blog_id INTEGER, user_id INTEGER, FOREIGN KEY(blog_id) REFERENCES blog(bid), FOREIGN KEY(user_id) REFERENCES user(id));
CREATE TABLE user_follow (user_id INTEGER, follower_id INTEGER, FOREIGN KEY(user_id) REFERENCES user(id), FOREIGN KEY(follower_id) REFERENCES user(id));

CREATE TABLE user_addi(uuid INTEGER PRIMARY KEY, age INTEGER, description TEXT);


INSERT INTO user_info VALUES (4, 'John', 'John');
INSERT INTO blog_info VALUES (4, 'John''s First Blog', 1, 'This is John''s First Blog');
INSERT INTO blog_like VALUES (1, 1);
INSERT INTO blog_fav VALUES (1, 1);

DELETE FROM user_info WHERE id > 4;
DELETE FROM user_addi WHERE uuid > 4;
DELETE FROM blog_info WHERE uid = 1;

ROLLBACK;

SELECT sql FROM sqlite_master WHERE type='table';

INSERT INTO blog_info VALUES (4, 'Wow im helping test the website !! )w)', 1, 'This a super long long mainly made to test. how this websote renders it. Hmmm im not really sure wat to put here. I wonder how many people weill ever see this? Wow that makes me kinda ssad. So many things are lost to the eternity. No way of ever knowing if legacy will ever live. Even a vile man like Hitker will be forgotten one day. In that case the sooner the better. Then again im not sure if that is a good idea.');

SELECT bid, btitle, bcontent, name FROM blog_info JOIN user_info on uid = id;

SELECT bid, btitle, bcontent, name FROM blog_info JOIN user_info on uid = id WHERE uid = 3;

SELECT bid, btitle, bcontent, name FROM blog_info JOIN user_info on uid = id WHERE btitle LIKE '%website%';

SELECT name,description FROM user_info JOIN user_addi on id = uuid;

INSERT INTO blog_info VALUES(0, 'This is a the deafult blog',2,'This is content')