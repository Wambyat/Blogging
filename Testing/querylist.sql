CREATE TABLE user_info(id INTEGER PRIMARY KEY, name varchar(20), password varchar(30));
CREATE TABLE blog_info(bid INTEGER PRIMARY KEY, btitle varchar(20), uid varchar(30), bcontent TEXT, FOREIGN KEY (uid) REFERENCES user_info(id));
CREATE TABLE blog_like(bid INTEGER,uid INTEGER );
CREATE TABLE blog_fav(bid INTEGER ,uid INTEGER );

INSERT INTO user_info VALUES (4, 'John', 'John');
INSERT INTO blog_info VALUES (4, 'John''s First Blog', 1, 'This is John''s First Blog');
INSERT INTO blog_like VALUES (1, 1);
INSERT INTO blog_fav VALUES (1, 1);
