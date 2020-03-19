-- ----------------------------
--  Table structure for `User`
-- ----------------------------
DROP TABLE IF EXISTS User;
-- SHOW WARNINGS;
CREATE TABLE User (
  user_id INT(10) NOT NULL,
  user_name varchar(100) NOT NULL,
  gender CHAR(1) DEFAULT NULL,
  last_refresh_time INT(10) NOT NULL,
  PRIMARY KEY(user_id)
);
