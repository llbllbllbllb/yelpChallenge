-- ----------------------------
--  Table structure for `User`
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
  latitude FLOAT 

  PRIMARY KEY(user_id)
);
