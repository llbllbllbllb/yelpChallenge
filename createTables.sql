
drop database if EXISTS yelp;
create database yelp;
use yelp;

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
  state VARCHAR(5),
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
  BYOBCorkage VARCHAR(100) DEFAULT NULL,
  DriveThru BOOLEAN DEFAULT NULL,
  Smoking VARCHAR(10) DEFAULT NULL,
  AgesAllowed VARCHAR(10) DEFAULT NULL,
  Corkage BOOLEAN DEFAULT NULL,
  BYOB BOOLEAN DEFAULT NULL,
  Open24Hours BOOLEAN DEFAULT NULL,
  RestaurantsCounterService BOOLEAN DEFAULT NULL,

  PRIMARY KEY(business_id),
  FOREIGN KEY(business_id) REFERENCES business(business_id)
);


-- ----------------------------
--  Table structure for `attrGoodForMeal`
-- ----------------------------
DROP TABLE IF EXISTS attrGoodForMeal;
-- SHOW WARNINGS;
CREATE TABLE attrGoodForMeal (
  business_id CHAR(22) NOT NULL,

  dessert BOOLEAN DEFAULT NULL,
  latenight BOOLEAN DEFAULT NULL,
  lunch BOOLEAN DEFAULT NULL,
  dinner BOOLEAN DEFAULT NULL,
  brunch BOOLEAN DEFAULT NULL,
  breakfast BOOLEAN DEFAULT NULL,

  PRIMARY KEY(business_id),
  FOREIGN KEY(business_id) REFERENCES business(business_id)

);


-- ----------------------------
--  Table structure for `attrBusinessParking`
-- ----------------------------
DROP TABLE IF EXISTS attrBusinessParking;
-- SHOW WARNINGS;
CREATE TABLE attrBusinessParking (
  business_id CHAR(22) NOT NULL,

  garage BOOLEAN DEFAULT NULL,
  street BOOLEAN DEFAULT NULL,
  validated BOOLEAN DEFAULT NULL,
  lot BOOLEAN DEFAULT NULL,
  valet BOOLEAN DEFAULT NULL,

  PRIMARY KEY(business_id),
  FOREIGN KEY(business_id) REFERENCES business(business_id)

);


-- ----------------------------
--  Table structure for `attrAmbience`
-- ----------------------------
DROP TABLE IF EXISTS attrAmbience;
-- SHOW WARNINGS;
CREATE TABLE attrAmbience (
  business_id CHAR(22) NOT NULL,

  romantic BOOLEAN DEFAULT NULL,
  intimate BOOLEAN DEFAULT NULL,
  classy BOOLEAN DEFAULT NULL,
  hipster BOOLEAN DEFAULT NULL,
  divey BOOLEAN DEFAULT NULL,
  touristy BOOLEAN DEFAULT NULL,
  trendy BOOLEAN DEFAULT NULL,
  upscale BOOLEAN DEFAULT NULL,
  casual BOOLEAN DEFAULT NULL,

  PRIMARY KEY(business_id),
  FOREIGN KEY(business_id) REFERENCES business(business_id)

);

-- ----------------------------
--  Table structure for `attrMusic`
-- ----------------------------
DROP TABLE IF EXISTS attrMusic;
-- SHOW WARNINGS;
CREATE TABLE attrMusic (
  business_id CHAR(22) NOT NULL,

  dj BOOLEAN DEFAULT NULL,
  background_music BOOLEAN DEFAULT NULL,
  no_music BOOLEAN DEFAULT NULL,
  jukebox BOOLEAN DEFAULT NULL,
  live BOOLEAN DEFAULT NULL,
  video BOOLEAN DEFAULT NULL,
  karaoke BOOLEAN DEFAULT NULL,

  PRIMARY KEY(business_id),
  FOREIGN KEY(business_id) REFERENCES business(business_id)

);


-- ----------------------------
--  Table structure for `attrBestNights`
-- ----------------------------
DROP TABLE IF EXISTS attrBestNights;
-- SHOW WARNINGS;
CREATE TABLE attrBestNights (
  business_id CHAR(22) NOT NULL,

  monday BOOLEAN DEFAULT NULL,
  tuesday BOOLEAN DEFAULT NULL,
  friday BOOLEAN DEFAULT NULL,
  wednesday BOOLEAN DEFAULT NULL,
  thursday BOOLEAN DEFAULT NULL,
  sunday BOOLEAN DEFAULT NULL,
  saturday BOOLEAN DEFAULT NULL,

  PRIMARY KEY(business_id),
  FOREIGN KEY(business_id) REFERENCES business(business_id)

);


-- ----------------------------
--  Table structure for `attrHairSpecializesIn`
-- ----------------------------
DROP TABLE IF EXISTS attrHairSpecializesIn;
-- SHOW WARNINGS;
CREATE TABLE attrHairSpecializesIn (
  business_id CHAR(22) NOT NULL,

  straightperms BOOLEAN DEFAULT NULL,
  coloring BOOLEAN DEFAULT NULL,
  extensions BOOLEAN DEFAULT NULL,
  africanamerican BOOLEAN DEFAULT NULL,
  curly BOOLEAN DEFAULT NULL,
  kids BOOLEAN DEFAULT NULL,
  perms BOOLEAN DEFAULT NULL,
  asian BOOLEAN DEFAULT NULL,

  PRIMARY KEY(business_id),
  FOREIGN KEY(business_id) REFERENCES business(business_id)

);


-- ----------------------------
--  Table structure for `attrDietaryRestrictions`
-- ----------------------------
DROP TABLE IF EXISTS attrDietaryRestrictions;
-- SHOW WARNINGS;
CREATE TABLE attrDietaryRestrictions (
  business_id CHAR(22) NOT NULL,

  dairy_free BOOLEAN DEFAULT NULL,
  gluten_free BOOLEAN DEFAULT NULL,
  vegan BOOLEAN DEFAULT NULL,
  kosher BOOLEAN DEFAULT NULL,
  halal BOOLEAN DEFAULT NULL,
  soy_free BOOLEAN DEFAULT NULL,
  vegetarian BOOLEAN DEFAULT NULL,

  PRIMARY KEY(business_id),
  FOREIGN KEY(business_id) REFERENCES business(business_id)

);




-- ----------------------------
--  Table structure for `categories`
-- ----------------------------
DROP TABLE IF EXISTS categories;
-- SHOW WARNINGS;
CREATE TABLE categories (
  business_id CHAR(22) NOT NULL,
  category VARCHAR(256) NOT NULL,

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
  FOREIGN KEY(friend_id) REFERENCES user(user_id)

);

-- ----------------------------
--  Table structure for `friendRequest`
-- ----------------------------
DROP TABLE IF EXISTS friendRequest;
-- SHOW WARNINGS;
CREATE TABLE friendRequest (
  user_id CHAR(22) NOT NULL,
  friend_id CHAR(22) NOT NULL,

  PRIMARY KEY(user_id, friend_id),
  FOREIGN KEY(user_id) REFERENCES user(user_id),
  FOREIGN KEY(friend_id) REFERENCES user(user_id)

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
  reviewDate DATE,
  reviewTime TIME,
  reviewText TEXT,

  useful INT DEFAULT 0,
  funny INT DEFAULT 0,
  cool INT DEFAULT 0,



  PRIMARY KEY(review_id),
  FOREIGN KEY(user_id) REFERENCES user(user_id),
  FOREIGN KEY(business_id) REFERENCES business(business_id)


);


-- ----------------------------
--  Table structure for `review`
-- ----------------------------
DROP TABLE IF EXISTS reviewRelation;
-- SHOW WARNINGS;
CREATE TABLE reviewRelation (
  review_id CHAR(22) NOT NULL,
  response_to_review_id CHAR(22) NOT NULL,

  PRIMARY KEY(review_id, response_to_review_id),
  FOREIGN KEY(review_id) REFERENCES review(review_id),
  FOREIGN KEY(response_to_review_id) REFERENCES review(review_id)
);



-- ----------------------------
--  Table structure for `checkin`
-- ----------------------------
DROP TABLE IF EXISTS checkin;
-- SHOW WARNINGS;
CREATE TABLE checkin (
  business_id CHAR(22) NOT NULL,
  checkinDate DATE NOT NULL,
  checkinTime TIME NOT NULL,

  PRIMARY KEY(business_id,checkinDate,checkinTime),
  FOREIGN KEY(business_id) REFERENCES business(business_id)

);

-- ----------------------------
--  Table structure for `tip`
-- ----------------------------
DROP TABLE IF EXISTS tip;
-- SHOW WARNINGS;
CREATE TABLE tip (
  tip_id INT NOT NULL AUTO_INCREMENT,
  business_id CHAR(22) NOT NULL,
  user_id CHAR(22) NOT NULL,

  tipText TEXT NOT NULL,
  postDate DATE NOT NULL,
  postTime TIME NOT NULL,
  compliment_count INT DEFAULT 0 NOT NULL,

  PRIMARY KEY(tip_id),
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

  caption TEXT,
  label VARCHAR(10),

  PRIMARY KEY(photo_id),
  FOREIGN KEY(business_id) REFERENCES business(business_id)


);

-- ----------------------------
--  Table structure for `group_info`
-- ----------------------------
DROP TABLE IF EXISTS group_info;
-- SHOW WARNINGS;
CREATE TABLE group_info (
  group_id CHAR(22) NOT NULL,
  name VARCHAR(200) NOT NULL,

  PRIMARY KEY(group_id)
);

-- ----------------------------
--  Table structure for `user_group`
-- ----------------------------
DROP TABLE IF EXISTS user_group;
-- SHOW WARNINGS;
CREATE TABLE user_group (
  group_id CHAR(22) NOT NULL,
  user_id CHAR(22) NOT NULL,

  PRIMARY KEY(group_id,user_id),
  FOREIGN KEY(user_id) REFERENCES user(user_id)
  FOREIGN KEY(group_id) REFERENCES group_info(group_id)
);


-- ----------------------------
--  Table structure for `user_follow_business`
-- ----------------------------
DROP TABLE IF EXISTS user_follow_business;
-- SHOW WARNINGS;
CREATE TABLE user_follow_business (
  user_id CHAR(22) NOT NULL,
  business_id CHAR(22) NOT NULL,

  PRIMARY KEY(user_id,business_id),
  FOREIGN KEY(user_id) REFERENCES user(user_id),
  FOREIGN KEY(business_id) REFERENCES business(business_id)
);
