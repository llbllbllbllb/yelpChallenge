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


  PRIMARY KEY(business_id)
);


-- ----------------------------
--  Table structure for `attributes`
-- ----------------------------
DROP TABLE IF EXISTS attributes;
-- SHOW WARNINGS;
CREATE TABLE attributes (
  business_id CHAR(22) NOT NULL,

  GoodForKids BOOLEAN DEFAULT NULL,
  RestaurantsReservations BOOLEAN DEFAULT NULL,
  Caters BOOLEAN DEFAULT NULL,
  NoiseLevel VARCHAR(10) DEFAULT NULL,
  RestaurantsTableService BOOLEAN DEFAULT NULL,
  RestaurantsTakeOut BOOLEAN DEFAULT NULL,
  RestaurantsPriceRange2 INT DEFAULT NULL,
  OutdoorSeating BOOLEAN DEFAULT NULL,
  BikeParking BOOLEAN DEFAULT NULL,
  HasTV BOOLEAN DEFAULT NULL,
  WiFi VARCHAR(5) DEFAULT NULL,
  Alcohol VARCHAR(20) DEFAULT NULL,
  RestaurantsAttire VARCHAR(10) DEFAULT NULL,
  RestaurantsGoodForGroups BOOLEAN DEFAULT NULL,
  RestaurantsDelivery BOOLEAN DEFAULT NULL,
  BusinessAcceptsCreditCards BOOLEAN DEFAULT NULL,
  BusinessAcceptsBitcoin BOOLEAN DEFAULT NULL,
  ByAppointmentOnly BOOLEAN DEFAULT NULL,
  AcceptsInsurance BOOLEAN DEFAULT NULL,
  GoodForDancing BOOLEAN DEFAULT NULL,
  CoatCheck BOOLEAN DEFAULT NULL,
  HappyHour BOOLEAN DEFAULT NULL,
  WheelchairAccessible BOOLEAN DEFAULT NULL,
  DogsAllowed BOOLEAN DEFAULT NULL,
  BYOBCorkage VARCHAR(10) DEFAULT NULL,
  DriveThru BOOLEAN DEFAULT NULL,
  Smoking VARCHAR(10) DEFAULT NULL,
  AgesAllowed VARCHAR(10) DEFAULT NULL,
  Corkage BOOLEAN DEFAULT NULL,
  BYOB BOOLEAN DEFAULT NULL,
  Open24Hours BOOLEAN DEFAULT NULL,
  RestaurantsCounterService BOOLEAN DEFAULT NULL,

  PRIMARY KEY(business_id)






);


-- ----------------------------
--  Table structure for `categories`
-- ----------------------------
DROP TABLE IF EXISTS categories;
-- SHOW WARNINGS;
CREATE TABLE categories (
  business_id CHAR(22) NOT NULL,
  category VARCHAR(30) NOT NULL,

  PRIMARY KEY(business_id,category),
  FOREIGN KEY(business_id) REFERENCES business(business_id)

);




-- ----------------------------
--  Table structure for `hours`
-- ----------------------------
DROP TABLE IF EXISTS hours;
-- SHOW WARNINGS;
CREATE TABLE hours (
  business_id CHAR(22) NOT NULL,

  mondayStart TIME,
  mondayEnd TIME,

  tuesdayStart TIME,
  tuesdayEnd TIME,

  wednesdayStart TIME,
  wednesdayEnd TIME,

  thursdayStart TIME,
  thursdayEnd TIME,

  fridayStart TIME,
  fridayEnd TIME,

  saturdayStart TIME,
  saturdayEnd TIME,

  sundayStart TIME,
  sundayEnd TIME,

  PRIMARY KEY(business_id),
  FOREIGN KEY(business_id) REFERENCES business(business_id)
);


-- ----------------------------
--  Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS user;
-- SHOW WARNINGS;
CREATE TABLE user (
  user_id CHAR(22) NOT NULL,
  name VARCHAR(100),
  review_count INT DEFAULT 0,
  yelping_since DATE,
  useful INT DEFAULT 0,
  funny INT DEFAULT 0,
  cool INT DEFAULT 0,
  fans INT DEFAULT 0,
  average_stars FLOAT,
  compliment_hot INT DEFAULT 0,
  compliment_more INT DEFAULT 0,
  compliment_profile INT DEFAULT 0,
  compliment_cute INT DEFAULT 0,
  compliment_list INT DEFAULT 0,
  compliment_note INT DEFAULT 0,
  compliment_plain INT DEFAULT 0,
  compliment_cool INT DEFAULT 0,
  compliment_funny INT DEFAULT 0,
  compliment_writer INT DEFAULT 0,
  compliment_photos INT DEFAULT 0,

  PRIMARY KEY(user_id)

);


-- ----------------------------
--  Table structure for `friend`
-- ----------------------------
DROP TABLE IF EXISTS friend;
-- SHOW WARNINGS;
CREATE TABLE friend (
  user_id CHAR(22) NOT NULL,
  friend_id CHAR(22) NOT NULL,

  PRIMARY KEY(user_id, friend_id),
  FOREIGN KEY(user_id) REFERENCES user(user_id),
  FOREIGN KEY(friend_id) REFERENCES user(friend_id),

);

-- ----------------------------
--  Table structure for `eliteYear`
-- ----------------------------
DROP TABLE IF EXISTS eliteYear;
-- SHOW WARNINGS;
CREATE TABLE eliteYear (
  user_id CHAR(22) NOT NULL,
  eliteYear INT(4) NOT NULL,

  PRIMARY KEY(user_id, eliteYear),
  FOREIGN KEY(user_id) REFERENCES user(user_id)

);


-- ----------------------------
--  Table structure for `review`
-- ----------------------------
DROP TABLE IF EXISTS review;
-- SHOW WARNINGS;
CREATE TABLE review (
  review_id CHAR(22) NOT NULL,

  user_id CHAR(22) NOT NULL,
  business_id CHAR(22) NOT NULL,

  stars INT NOT NULL,
  reviewDate DATE NOT NULL,
  reviewText VARCHAR(200),

  useful INT DEFAULT 0,
  funny INT DEFAULT 0,
  cool INT DEFAULT 0,



  PRIMARY KEY(review_id),
  FOREIGN KEY(user_id) REFERENCES user(user_id),
  FOREIGN KEY(business_id) REFERENCES business(business_id)


);





-- ----------------------------
--  Table structure for `checkin`
-- ----------------------------
DROP TABLE IF EXISTS checkin;
-- SHOW WARNINGS;
CREATE TABLE checkin (
  business_id CHAR(22) NOT NULL,
  checkinDate DATE NOT NULL,

  PRIMARY KEY(business_id,checkinDate),
  FOREIGN KEY(business_id) REFERENCES business(business_id)

);

-- ----------------------------
--  Table structure for `tip`
-- ----------------------------
DROP TABLE IF EXISTS tip;
-- SHOW WARNINGS;
CREATE TABLE tip (
  business_id CHAR(22) NOT NULL,
  user_id CHAR(22) NOT NULL,

  tipText VARCHAR(200) NOT NULL,
  postDate DATE NOT NULL,
  compliment_count INT DEFAULT 0 NOT NULL,

  PRIMARY KEY(business_id, user_id),
  FOREIGN KEY(business_id) REFERENCES business(business_id),
  FOREIGN KEY(user_id) REFERENCES user(user_id)

);


-- ----------------------------
--  Table structure for `photo`
-- ----------------------------
DROP TABLE IF EXISTS photo;
-- SHOW WARNINGS;
CREATE TABLE photo (
  photo_id CHAR(22) NOT NULL,
  business_id CHAR(22) NOT NULL,

  caption VARCHAR(100),
  label VARCHAR(10),

  PRIMARY KEY(photo_id),
  FOREIGN KEY(business_id) REFERENCES business(business_id)


);
