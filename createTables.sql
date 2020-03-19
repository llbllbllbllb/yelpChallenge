-- ----------------------------
--  Table structure for `business`
-- ----------------------------
DROP TABLE IF EXISTS business;
-- SHOW WARNINGS;
CREATE TABLE business (
  business_id CHAR(22) NOT NULL,
  name VARCHAR(100),
  address VARCHAR(200),
  city VARCHAR(50),
  state CHAR(2),
  postal_code VARCHAR(10),
  latitude FLOAT,
  longitude FLOAT,
  stars FLOAT,
  review_count FLOAT,
  is_open INT,


  PRIMARY KEY(user_id)
);


-- ----------------------------
--  Table structure for `attributes`
-- ----------------------------
DROP TABLE IF EXISTS attributes;
-- SHOW WARNINGS;
CREATE TABLE attributes (

);


-- ----------------------------
--  Table structure for `categories`
-- ----------------------------
DROP TABLE IF EXISTS categories;
-- SHOW WARNINGS;
CREATE TABLE categories (

);




-- ----------------------------
--  Table structure for `hours`
-- ----------------------------
DROP TABLE IF EXISTS hours;
-- SHOW WARNINGS;
CREATE TABLE hours (

);
