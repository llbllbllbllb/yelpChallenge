# **ECE656 Project Report: A Simple Social Network (with Yelp Dataset)**

Student Name: Libang Liang, Student ID: 20662701

Student Name: Zhiming Lin, Student ID: 20835645

#### 0. Introduction

In this project, we built a simple social network. First we created entity-relationship model for this network, then we translated our ER Model into relational database design. We populated Yelp Dataset using python generated sql files, and wrote list of APIs that allow client to initial a post on topics, follow other users, form groups, refresh posts, reply posts etc. using Java Spring Boot framework. Tests on different written APIs are also written.

#### 1. ER Model
<img src="ER Model.png" alt="ER Model" style="zoom:50%;" />





In the entity-relationship schema, we have 5 entities: User, Business, Review, Photo and Group. One user can have $0$ to $N$ friend(s), so there is a many-to-many relationships between users of Is-Friend relation. On the other hand, a user can be in $0$ to $N$ group(s) while a group must has at least 2 members. User can follow $0$ to $N$ Business while Business can be followed by $0$ to $N$ users,  so there is a many-to-many relationship for User-Follow-Business relation. The same situation applies to Tip relation: User can write $0$ to $N$ tips on a Business and Business can hold tips from many users. There is a ternary relationships between User, Review and Business, which means user can write review on a business. Also, review itself can be replied by another review, so there is a Reply-to relation. Finally, Business can has $0$ to $N$ photos while one photo must belong to one Business, so a Is-Photo-Of relationship is a one to many relation.



#### 2. Create Tables

In order to satify all the requirements and functions, we create the tables as follow:

User:

```mysql
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
```

One user can have zero to many friends. One user can be friend of zero to many friends. 

Therefore, friend table:

```mysql
DROP TABLE IF EXISTS friend;
-- SHOW WARNINGS;
CREATE TABLE friend (
  user_id CHAR(22) NOT NULL,
  friend_id CHAR(22) NOT NULL,

  PRIMARY KEY(user_id, friend_id),
  FOREIGN KEY(user_id) REFERENCES user(user_id),
  FOREIGN KEY(friend_id) REFERENCES user(user_id)

);
```

Also, one user can deny or accept the friend request from other users. FriendRequest table is needed to implement such function.

```mysql
DROP TABLE IF EXISTS friendRequest;
-- SHOW WARNINGS;
CREATE TABLE friendRequest (
  user_id CHAR(22) NOT NULL,
  friend_id CHAR(22) NOT NULL,

  PRIMARY KEY(user_id, friend_id),
  FOREIGN KEY(user_id) REFERENCES user(user_id),
  FOREIGN KEY(friend_id) REFERENCES user(user_id)

);
```

One user can be elected in different years, it would be better to seperate them into different tables.

eliteYear:

```mysql
DROP TABLE IF EXISTS eliteYear;
-- SHOW WARNINGS;
CREATE TABLE eliteYear (
  user_id CHAR(22) NOT NULL,
  eliteYear INT(4) NOT NULL,

  PRIMARY KEY(user_id, eliteYear),
  FOREIGN KEY(user_id) REFERENCES user(user_id)

);
```

One user can form zero to many groups. One group must contain one user. Every group has its own name. In order to reduce duplications, we create two tables for groups, user_group and group_info.

User_group table: 

```mysql
DROP TABLE IF EXISTS user_group;
-- SHOW WARNINGS;
CREATE TABLE user_group (
  group_id CHAR(22) NOT NULL,
  user_id CHAR(22) NOT NULL,

  PRIMARY KEY(group_id,user_id),
  FOREIGN KEY(user_id) REFERENCES user(user_id)
  FOREIGN KEY(group_id) REFERENCES group_info(group_id)
);
```

group_info table:

```mysql
DROP TABLE IF EXISTS group_info;
-- SHOW WARNINGS;
CREATE TABLE group_info (
  group_id CHAR(22) NOT NULL,
  name VARCHAR(200) NOT NULL,

  PRIMARY KEY(group_id)
);
```



For business (restaurants):

```mysql
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
```

Because every business has different attributes. The attribute may be mulitvalues or single value. Hence, we create a table for single attribute and tables for multivalues attributes.



##### Single attribute

```mysql
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
```



##### Multivalues attribute

GoodForMeal

```mysql
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
```



The attrBusinessParking

```mysql
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
```



attrAmbience

```mysql
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
```



attrMusic

```mysql
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
```



attrBestNights

```mysql
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
```



attrHairSpecializesIn

```mysql
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
```



attrDietaryRestrictions

```mysql
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
```



categories

```mysql
DROP TABLE IF EXISTS categories;
-- SHOW WARNINGS;
CREATE TABLE categories (
  business_id CHAR(22) NOT NULL,
  category VARCHAR(256) NOT NULL,

  PRIMARY KEY(business_id,category),
  FOREIGN KEY(business_id) REFERENCES business(business_id)

);
```



hours

```mysql
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
```



One business can have zero to many photos. One photo can only belong to one business.

```mysql
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
```



One user can follow zero to many businesses. While, one business can be followed by zero to many users.

```mysql
DROP TABLE IF EXISTS user_follow_business;
-- SHOW WARNINGS;
CREATE TABLE user_follow_business (
  user_id CHAR(22) NOT NULL,
  business_id CHAR(22) NOT NULL,

  PRIMARY KEY(user_id,business_id),
  FOREIGN KEY(user_id) REFERENCES user(user_id),
  FOREIGN KEY(business_id) REFERENCES business(business_id)
);
```



One business can be checked in multiple times.

checkin

```mysql
DROP TABLE IF EXISTS checkin;
-- SHOW WARNINGS;
CREATE TABLE checkin (
  business_id CHAR(22) NOT NULL,
  checkinDate DATE NOT NULL,
  checkinTime TIME NOT NULL,

  PRIMARY KEY(business_id,checkinDate,checkinTime),
  FOREIGN KEY(business_id) REFERENCES business(business_id)

);
```



One user can write zero to many tips for one business. one business can be written tips by zero to many users.

 tip

```mysql
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
```



One user can write zero to many reviews about one business. One review can rely to one reviews. one review can be replied by multiple reviews.

```mysql
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
```

reviewRelation:

```mysql
DROP TABLE IF EXISTS reviewRelation;
-- SHOW WARNINGS;
CREATE TABLE reviewRelation (
  review_id CHAR(22) NOT NULL,
  response_to_review_id CHAR(22) NOT NULL,

  PRIMARY KEY(review_id, response_to_review_id),
  FOREIGN KEY(review_id) REFERENCES review(review_id),
  FOREIGN KEY(response_to_review_id) REFERENCES review(review_id)
);
```



Also, user_last_refresh table is created to satisfy that user can determine what posts have been added by people and/or topics that they are following since they last read from those people/topics:

user_last_refresh

```mysql
DROP TABLE IF EXISTS user_last_refresh;
-- SHOW WARNINGS;
CREATE TABLE user_last_refresh (
  user_id CHAR(22) NOT NULL,
  refresh_time TIME NOT NULL,
  refresh_date DATE NOT NULL,

  PRIMARY KEY(user_id),
  FOREIGN KEY(user_id) REFERENCES user(user_id)
);
```



#### 3. Populating the data

Total size of the JSON data: 9.8GB

We first used Python Script to generate SQL batched insert statement to insert large JSON file.

**Implementation** 

Take populating review as an example:

```python
def populateReview(review_file_path):
    if os.path.exists("generateReview.sql"):
        os.remove("generateReview.sql")
    gff =  open("generateReview.sql", "a")
    gff.write("DELETE FROM review;\n")
    gff.write("BEGIN;\n")

    count = 0
    set_batch_size = 100
    batch_size = set_batch_size

    file_count = 1
    # test_size = 100000
    with open(review_file_path) as f:
        print("test")
        query = "\n INSERT INTO review (review_id,user_id, business_id,stars,reviewDate,reviewTime,reviewText,useful,funny,cool) VALUES "
        for line in f:
            if batch_size == set_batch_size:
                gff.write(query)
            count+=1
            print(" %d / 6685900"%(count), end='\r')
            data = json.loads(line)

            review_id = data["review_id"]
            user_id = data["user_id"]
            business_id = data["business_id"]
            stars = data["stars"]
            date_time = data["date"]
            reviewText = data["text"]
            useful = data["useful"]
            funny = data["funny"]
            cool = data["cool"]

            reviewDate,reviewTime = date_time.split()

            reviewText = reviewText.replace('"',"")
            reviewText = reviewText.replace(';',"")
            reviewText = reviewText.replace('\\', '/ ')

            value = "(\'"+str(review_id)+"\',"+"\'"+ str(user_id)+"\',"+"\'"+ str(business_id)+"\',"+"\'"+ str(stars)+"\',"+"\'"+ str(reviewDate)+"\',"+"\'"+str(reviewTime)+"\',"+"\""+ str(reviewText)+"\","+"\'"+ str(useful)+"\',"+"\'"+ str(funny)+"\',"+"\'"+ str(cool)+"\')"

            batch_size-=1;
            if batch_size == 0:
                value += ";"
                batch_size = set_batch_size
            else:
                value += ","

            gff.write(value)


    gff.write(";")
    gff.write("\nCOMMIT;")
    gff.close()
```

We first create an empty sql file. Then we read the JSON file in batches. In the review text object, we replaced the ambiguous characters to the mysql statements. we then write the SQL statements into the sql files. Finally We source this .sql file in the mysql session.

Other scripts can be seen in populate.py.





#### 4. Client(README)

This part is done in Spring Boot, user can be type in corresponding address to call the APIs and complete functions they want.

We created set of APIs using Java with Spring Boot Framwork. User can do the following functions:

1. Register
   User should be able to register a new user account by providing a user name, a unique user id is created and returned to the user.

   ```java
       @PostMapping("/register/{name}")
       public String register(@PathVariable String name) {
           user = User.getInstance();
           user.setUser_name(name);
           int code = user.newUser(conn);
           if (code == 1) {
               return "Register successfully. Your userID is " + user.getUser_id() + "\n";
           } else {
               return null;
           }
       }
   ```
   
   ```java
       public int newUser(Connection conn) {
           String user_id = generateUniqueId();
           this.user_id = user_id;
           LocalDate yelping_since = LocalDate.now();
           String sql = "INSERT INTO user (user_id, name, yelping_since) " +
                   "VALUES (" + "\"" + user_id + "\", \"" + this.user_name + "\" ,\"" + yelping_since + "\");";
           System.out.println(sql);
           boolean status = insertSQL(sql, conn);
           if (status == true) {
               System.out.println("Registration successfully!");
               return 1;
           } else {
               System.out.println("Please try again");
               return 0;
           }
       }
   ```
   
   
   
2. Login
   User should be able to login ther account by providing their user id.

   ```java
       @GetMapping("/login/{user_id}")
       public String login(@PathVariable String user_id) throws SQLException {
           user = User.getInstance();
           user.setUser_id(user_id);
           user.setUser_name("");
           int code = user.login(user_id,conn);
           if(code == -1){
               return "Invalid User ID, please try again.\n";
           }
           else if(code == 0){
   
               return "Login Successfully. Your UserID is: " + user_id+ "\n";
           }
           else {
               return "Please Try Again.\n";
           }
   
       }
   ```

   ```java
       public int login(String user_id, Connection conn) throws SQLException {
           String sql = "SELECT user_id from user where user_id = \'" +  user_id + "\';";
           System.out.println(sql);
   
           ResultSet rs = executeSQL(sql, conn);
           if(!(rs.isBeforeFirst() )) {
   //            not exist
               return -1;
           }
           else{
               return 0;
           }
   
       }
   ```

   

3. Refresh new reviews if they followed any business(restaurant) or friends
   User should be able to look at their unseen reviews based on the 1. business(restaurant) they followed, 2. freinds they have.

   ```java
       @RequestMapping("/refresh/userId={user_id}")
       public ArrayList<review> refresh(@PathVariable String user_id) throws SQLException {
           if(user == null) {
               return null;
           } else{
               ArrayList<review> content = user.refreshReview(user.getUser_id(),conn);
               return content;
           }
       }
   ```

   ```java
       public ArrayList<review> refreshReview(String user_id,Connection conn) throws SQLException {
   
           //user should be able to refresh new followBusiness(Restaurant new reviews) / friend written reviews
   
           // get refresh time. table: user_last_refresh
           String get_refresh_time_sql = "SELECT refresh_time, refresh_date from user_last_refresh where user_id = \'" + user_id + "\';";
   
           ResultSet rs = executeSQL(get_refresh_time_sql, conn);
   
           String oldRefreshtime = "";
           String oldRefreshdate = "";
           while (rs.next()) {
               oldRefreshtime = rs.getString("refresh_time");
               oldRefreshdate = rs.getString("refresh_date");
           }
   
   
           //get current date and time
           LocalDateTime curTime = LocalDateTime.now();
           DateTimeFormatter dateFormat = DateTimeFormatter.ofPattern("yyyy-MM-dd");
           DateTimeFormatter timeFormat = DateTimeFormatter.ofPattern("HH:mm:ss");
           String newRefreshDate = curTime.format(dateFormat);
           String newRefreshTime = curTime.format(timeFormat);
   
           // if time date not exist, load all
           System.out.println("oldRefreshTime: " + oldRefreshtime);
           System.out.println("oldRefreshdate: " + oldRefreshdate);
           if (oldRefreshtime == "" || oldRefreshdate == "") {
               oldRefreshtime = "00:00:00";
               oldRefreshdate = "1900-01-01";
           }
   
           String get_review_sql =
                   "SELECT * from\n" +
                           "(SELECT * from\n" +
                           "(SELECT * from review where\n" +
                           "user_id in (SELECT friend_id from friend where user_id = \'" + user_id + "\') AND reviewDate > CAST(\'" + oldRefreshdate + "\' as DATE) AND reviewTime > CAST(\'" + oldRefreshtime + "\' as TIME)\n" +
                           "UNION\n" +
                           "SELECT * from review where\n" +
                           "business_id in (SELECT business_id from user_follow_business where user_id = \'" + user_id + "\') AND reviewDate > CAST(\'" + oldRefreshdate + "\' as DATE) AND reviewTime > CAST(\'" + oldRefreshtime + "\' as TIME)\n" +
                           "ORDER BY reviewDate,reviewTime) A\n" +
                           "natural join\n" +
                           "(SELECT user_id,name as username from user) B) C\n" +
                           "natural join\n" +
                           "(SELECT business_id,name as businessname from business) D;";
   
           rs = executeSQL(get_review_sql, conn);
   
   
           String review_id = "";
           String business_id = "";
           String friend_user_id = "";
           String username = "";
           String businessname = "";
           int stars = 0;
           String reviewDate = "";
           String reviewTime = "";
           String reviewText = "";
           int useful = 0;
           int funny = 0;
           int cool = 0;
   
           ArrayList<review> review_list = new ArrayList<review>();
           while (rs.next()) {
               review_id = rs.getString("review_id");
               business_id = rs.getString("business_id");
               friend_user_id = rs.getString("user_id");
               username = rs.getString("username");
               businessname = rs.getString("businessname");
               stars = rs.getInt("stars");
               reviewDate = rs.getString("reviewDate");
               reviewTime = rs.getString("reviewTime");
               reviewText = rs.getString("reviewText");
               useful = rs.getInt("useful");
               funny = rs.getInt("funny");
               cool = rs.getInt("cool");
   
               review tmp = new review(review_id, business_id, user_id, username, businessname, stars, reviewDate, reviewTime, reviewText, useful, funny, cool);
               review_list.add(tmp);
   
           }
           // if time date not exist
           if (oldRefreshtime == "00:00:00" && oldRefreshdate == "1900-01-01") {
               String update_refresh_time_sql = "INSERT INTO user_last_refresh (user_id, refresh_time, refresh_date) VALUES " +
                       "(\'" + user_id + "\',\'" + newRefreshTime + "\',\'" + newRefreshDate + "\');";
               System.out.println(update_refresh_time_sql);
               insertSQL(update_refresh_time_sql, conn);
           }
           else{
               String update_refresh_time_sql = "UPDATE user_last_refresh set refresh_time = \'" + newRefreshTime + "\', refresh_date = \'" + newRefreshDate + "\' where user_id = \'" + user_id + "\';";
               System.out.println(update_refresh_time_sql);
               insertSQL(update_refresh_time_sql, conn);
           }
   
   
           return review_list;
   
       }
   ```

   

4. Make friend request

   User should be able to make friend request if they can provide friend's user id.

   ```java
       @GetMapping("/addFriendRequest/{friendRequest_id}")
       public String addFriendRequest(@PathVariable String friendRequest_id) {
           if (user == null) {
               return "please register firstly.\n";
           } else {
               int code = user.addFriendRequest(friendRequest_id, conn);
               if (code == 1) {
                   return "Friend request sent. \n";
               } else {
                   return "Please try again. \n";
               }
           }
       }
   ```

   ```java
       public int addFriendRequest(String friendRequest_id, Connection conn) {
           String query = "INSERT INTO friendRequest " +
                   "(user_id, friend_id) VALUES (\"" + this.user_id + "\", \"" + friendRequest_id + "\");";
           System.out.println(query);
           Boolean status = insertSQL(query, conn);
           if (status == true) {
               System.out.println("Friend request sent");
               return 1;
           } else {
               System.out.println("Please try again");
               return 0;
           }
       }
   ```

   

5. Accept/Reject friend request
   User should be able to accept or reject any pending friend request.

   ```java
       @GetMapping("/rejectFriendRequest/{friendRequest_id}")
       public String rejectFriendRequest(@PathVariable String friendRequest_id) {
           if (user == null) {
               return "please register firstly. \n";
           } else {
               int code = user.rejectFriendRequest(friendRequest_id, conn);
               if (code == 1) {
                   return "Friend request rejected. \n";
               } else {
                   return "Please try again. \n";
               }
           }
       }
   
       @GetMapping("/acceptFriendRequest/{friendRequest_id}")
       public String acceptFriendRequest(@PathVariable String friendRequest_id) throws SQLException {
           if (user == null) {
               return "please register firstly.\n";
           } else {
               int code = user.acceptFriendRequest(friendRequest_id, conn);
               if (code == 1) {
                   return "Accept friend request successfully. \n";
               } else {
                   return "Please try again. \n";
               }
           }
       }
   ```

   ```java
       public int rejectFriendRequest(String friendRequest_id, Connection conn) {
   
           String query = "DELETE FROM friendRequest WHERE user_id = \"" + friendRequest_id + "\";";
   
           System.out.println(query);
           Boolean status = insertSQL(query, conn);
           if (status == true) {
               System.out.println("Friend request rejected");
               return 1;
           } else {
               System.out.println("Please try again");
               return 0;
           }
       }
   
       public int acceptFriendRequest(String friend_id, Connection conn) throws SQLException {
   
           int code = 0;
           String query1 = "INSERT INTO friend " +
                   "VALUES (" + "\"" + this.user_id + "\", \"" + friend_id + "\"), " +
                   "(\"" + friend_id + "\", \"" + this.user_id + "\");";
           String query2 = "DELETE FROM friendRequest WHERE user_id = \"" + friend_id + "\";";
   
           System.out.println(query1);
           System.out.println(query2);
           try {
               conn.setAutoCommit(false);
               Boolean status1 = insertSQL(query1, conn);
               Boolean status2 = insertSQL(query2, conn);
               if (!status1 || !status2) {
                   code = 0;
                   throw new SQLException("Please try again");
               }
               conn.commit();
               System.out.println("Accept friend request successfully");
               code = 1;
           } catch (SQLException e) {
               e.printStackTrace();
               conn.rollback();
           } finally {
               conn.setAutoCommit(true);
               return code;
           }
       }
   ```

   

6. Vote(useful, funny, cool) review
   User should be able to vote reviews if they can provide the review id and the type of vote.

   ```java
       @GetMapping("/vote/review_id={review_id}&&type={i}")
       public String vote(@PathVariable String review_id, @PathVariable int i) throws SQLException {
           System.out.println(review_id);
           System.out.println(i);
           if (user == null) {
               return "please register firstly. \n";
           } else {
               int code = user.vote(review_id, i, conn);
               if (code == 1) {
                   return "vote successfully. \n";
               } else {
                   return "Please try again. \n";
               }
           }
       }
   ```

   ```java
       public int vote(String review_id, int i, Connection conn) throws SQLException {
           int code = 0;
           String type = null;
           if (i == 0) {
               type = "useful";
           } else if (i == 1) {
               type = "funny";
           } else if (i == 2) {
               type = "cool";
           }
   //        String user = "0T8Nted2-45Q47vX7S7=2X";
           if (type != null) {
               String query1 = "UPDATE user SET " + type + " = " +
                       "IF (" + type + " is null, 1, " + type + " + 1) WHERE user_id = \"" + this.user_id + "\";";
               String query2 = "UPDATE review SET " + type + " = " +
                       "IF (" + type + " is null, 1, " + type + " + 1) WHERE review_id = \"" + review_id + "\";";
               System.out.println(query1);
               System.out.println(query2);
               try {
                   conn.setAutoCommit(false);
                   Boolean status1 = insertSQL(query1, conn);
                   Boolean status2 = insertSQL(query2, conn);
                   if (!status1 || !status2) {
                       throw new SQLException("Please try again");
                   }
                   conn.commit();
                   System.out.println("vote successfully");
                   code = 1;
               } catch (SQLException e) {
                   conn.rollback();
                   e.printStackTrace();
               } finally {
                   conn.setAutoCommit(true);
                   return code;
               }
           }
           return code;
       }
   ```

   

7. Follow User
   User should be able to follow user.

   ```java
       @GetMapping("/follow/user/{user_id}")
       public String followUser(@PathVariable String user_id) {
           if (user == null) {
               return "Please register firstly. \n";
           } else {
               int code = user.followUser(user_id, conn);
               if (code == 1) {
                   return "follow successfully. \n";
               } else {
                   return "Please try again. \n";
               }
           }
       }
   ```

   ```java
       public int followUser(String user_id, Connection conn) {
           String sql = "UPDATE user SET fans = " +
                   "IF (fans is null, 1, fans + 1) WHERE user_id = \"" + user_id + "\";";
           Boolean status = insertSQL(sql, conn);
           if (status == true) {
               System.out.println("follow successfully");
               return 1;
           } else {
               System.out.println("Please try again");
               return 0;
           }
       }
   ```

   

8. Choose Elite User
   User could be chosen to be elite user for specific year.

   ```java
       @GetMapping("/eliteuser/{user_id}")
       public String eliteUser(@PathVariable String user_id) {
           if (user == null) {
               return "Please register firstly. \n";
           } else {
               int code = user.eliteUser(user_id, conn);
               if (code == 1) {
                   return "Elect user as elite user this year successfully. \n";
               } else {
                   return "Please try again. \n";
               }
           }
       }
   ```

   ```java
       public int eliteUser(String user_id, Connection conn) {
           int currentYear = Year.now().getValue();
           String sql = "INSERT INTO eliteYear VALUES(\"" + user_id + "\", \"" + currentYear + "\");";
           System.out.println(sql);
   
           Boolean status = insertSQL(sql, conn);
           if (status == true) {
               System.out.println("Elect user successfully");
               return 1;
           } else {
               System.out.println("Please try again");
               return 0;
           }
       }
   ```

   

9. Reply Review
   User should be able to reply a review if they can provide the original review id.

   ```java
       @GetMapping("/reply/review/businessId={business_id}&&stars={stars}&&text={reviewText}&&responseTo={response_to_review_id}")
       public String replyReview(@PathVariable String business_id, @PathVariable int stars,
                                 @PathVariable String reviewText, @PathVariable String response_to_review_id) throws SQLException {
           if (user == null) {
               return "Please register firstly. \n";
           } else {
               int code = user.replyReview(business_id, stars, reviewText, response_to_review_id, conn);
               if (code == 1) {
                   return "reply successfully. \n";
               } else {
                   return "Please try again. \n";
               }
           }
       }
   ```

   ```java
       public int replyReview(String business_id, int stars,
                              String reviewText, String response_to_review_id, Connection conn) throws SQLException {
           int code = 0;
           String review_id = generateUniqueId();
           String user_id = this.user_id;
           DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");
           LocalDateTime now = LocalDateTime.now();
           String tmp = dtf.format(now);
           String[] tmp_split = tmp.split(" ");
           String date = tmp_split[0];
           String time = tmp_split[1];
   
           // replace some text to avoid insert failure
           reviewText = reviewText.replaceAll("\"", "");
   
           reviewText = reviewText.replaceAll("\\\\", "/");
           reviewText = reviewText.replaceAll(";", " ");
   
           String query1 = "INSERT INTO review (review_id, user_id, business_id, stars, reviewDate, reviewTime, reviewText) " +
                   "VALUES (\"" + review_id + "\", \"" + user_id + "\", \"" + business_id + "\", " +
                   stars + ", \"" + date + "\", \"" + time + "\", \"" + reviewText + "\");";
           String query2 = "INSERT INTO reviewRelation(review_id,response_to_review_id) VALUES (\"" + review_id + "\", \"" + response_to_review_id + "\");";
   
           System.out.println(query1);
           System.out.println(query2);
           try {
               conn.setAutoCommit(false);
               Boolean status1 = insertSQL(query1, conn);
               Boolean status2 = insertSQL(query2, conn);
               if (!status1 || !status2) {
                   throw new SQLException("Please try again");
               }
               conn.commit();
               System.out.println("reply successfully");
               code = 1;
           } catch (SQLException e) {
               conn.rollback();
               e.printStackTrace();
           } finally {
               conn.setAutoCommit(true);
               return code;
           }
   
       }
   ```

   

10. Upvote a Tip
	User should be able to upvote a tip if they can provide tip id.

	```java
	    @GetMapping("/compliment/tip/tipID={tip_id}&&compliment={i}")
	    public String complimentTip(@PathVariable String tip_id, @PathVariable int i) throws SQLException {
	        if (user == null) {
	            return "Please register firstly. \n";
	        } else {
	            int code = user.complimentTip(tip_id, i, conn);
	            if (code == 1) {
	                return "compliment tip successfully. \n";
	            } else {
	                return "Please try again. \n";
	            }
	        }
	    }
	```

	```java
	    public int complimentTip(String tip_id, int i, Connection conn) throws SQLException {
	        int code = 0;
	        String compliment = null;
	        String[] compliments = {"compliment_hot", "compliment_more", "compliment_profile", "compliment_cute", "compliment_list", "compliment_note", "compliment_plain", "compliment_cool", "compliment_funny", "compliment_writer", "compliment_photos"};
	        if (i >= 0 && i <= 10) {
	            compliment = compliments[i];
	        }
	        if (compliment != null) {
	            String query = "UPDATE tip SET compliment_count = compliment_count + 1 where tip_id = \'" + tip_id + "\';";
	            String query2 = "UPDATE user SET " + compliment + " = " +
	                    "IF (" + compliment + " is null, 1, " + compliment + " + 1) WHERE " +
	                    "user_id = (SELECT user_id FROM tip WHERE tip_id = \"" + tip_id + "\");";
	            System.out.println(query);
	            System.out.println(query2);
	            try {
	                conn.setAutoCommit(false);
	                Boolean status1 = insertSQL(query, conn);
	                Boolean status2 = insertSQL(query2, conn);
	                if (!status1 || !status2) {
	                    throw new SQLException("Please try again");
	                }
	                conn.commit();
	                System.out.println("compliment tip successfully");
	                code = 1;
	            } catch (SQLException e) {
	                conn.rollback();
	                e.printStackTrace();
	            } finally {
	                conn.setAutoCommit(true);
	                return code;
	            }
	        }
	        return code;
	    }
	```

	

11. Create a Group
	User should be able to create a group if they can provide list of user id(s).

	```java
	    @PostMapping("/creategroup")
	    public String createGroup(@RequestBody CreateGroupBean createGroupBean) throws SQLException {
	        if (user == null) {
	            return "Please register firstly. \n";
	        } else {
	            ArrayList<String> friends = createGroupBean.getFriends();
	            String groupName = createGroupBean.getGroupName();
	            int code = user.createGroup(groupName, friends, conn);
	            if (code == 1) {
	                return "create group successfully. \n";
	            } else {
	                return "Please try again. \n";
	            }
	        }
	    }
	```

	```java
	    public int createGroup(String groupname, ArrayList<String> friends, Connection conn) throws SQLException {
	        int code = 0;
	        if (groupname == null || groupname.length() == 0) {
	            System.out.println("Error: Empty group name.");
	            return code;
	        }
	
	        String group_id = generateUniqueId();
	
	        String sql = "INSERT INTO group_info (group_id,name) VALUES (\'" + group_id + "\',\'" + groupname + "\');";
	        String sql2 = "INSERT INTO user_group (group_id,user_id) VALUES (\'" + group_id + "\',\'" + this.user_id + "\');";
	
	        try {
	            conn.setAutoCommit(false);
	            Boolean status = insertSQL(sql, conn);
	            Boolean status2 = insertSQL(sql2, conn);
	            if (!status || !status2) {
	                throw new SQLException("Can not create group, Please try again");
	            }
	            for (int i = 0; i < friends.size(); i++) {
	                String query = "INSERT INTO user_group (group_id,user_id) VALUES (\'" + group_id + "\',\'" + friends.get(i) + "\');";
	                Boolean status3 = insertSQL(query, conn);
	                if (!status3) {
	                    throw new SQLException("Can not add friends, Please try again");
	                }
	            }
	            conn.commit();
	            System.out.println("create group successfully");
	            code = 1;
	        } catch (SQLException e) {
	            conn.rollback();
	            e.printStackTrace();
	        } finally {
	            conn.setAutoCommit(true);
	            return code;
	        }
	
	    }
	```

	

12. Join an existing group
	User should be able to join an existing group if they can provide a group id.

	```java
	    @GetMapping("/join/group/groupID='{group_id}'")
	    public String joinGroup(@PathVariable String group_id) throws SQLException {
	        if (user == null) {
	            return "Please register firstly. \n";
	        } else {
	            int code = user.joinGroup(group_id, conn);
	            if (code == 1) {
	                return "join group successfully. \n";
	            } else {
	                return "Please try again. \n";
	            }
	        }
	    }
	```

	```java
	    public int joinGroup(String group_id, Connection conn) throws SQLException {
	        int code = 0;
	        String sql = "INSERT INTO user_group (group_id,user_id) VALUES (\'" + group_id + "\',\'" + this.user_id + "\');";
	
	        try {
	            Boolean status = insertSQL(sql, conn);
	            if (!status) {
	                throw new SQLException("Can not join group, Please try again");
	            }
	            conn.commit();
	            System.out.println("Joined group successfully");
	            code = 1;
	
	        } catch (SQLException e) {
	            e.printStackTrace();
	            return code;
	        }
	        return code;
	    }
	```

	

13. Follow a Business(Restaurant)
	User should be able to follow a business(restaurant) if they can provide the business id.

	```java
	    @GetMapping("/follow/restaurant/businessId='{business_id}'")
	    public String followBusiness(@PathVariable String business_id) throws SQLException {
	        if (user == null) {
	            return "Please register firstly. \n";
	        } else {
	            int code = user.followBusiness(business_id, conn);
	            if (code == 1) {
	                return "Follow restaurant successfully \n";
	            } else {
	                return "Please try again. \n";
	            }
	        }
	    }
	```

	```java
	    public int followBusiness(String business_id, Connection conn) throws SQLException {
	        int code = 0;
	        String sql = "INSERT INTO user_follow_business (user_id,business_id) VALUES (\'" + this.user_id + "\',\'" + business_id + "\');";
	        System.out.println(sql);
	        try {
	            Boolean status = insertSQL(sql, conn);
	            if (!status) {
	                throw new SQLException("Can not follow restaurant, Please try again");
	            }
	//            conn.commit();
	            System.out.println("Follow restaurant successfully");
	            code = 1;
	
	        } catch (SQLException e) {
	//            conn.rollback();
	            e.printStackTrace();
	            return code;
	        }
	        return code;
	    }
	```

	

14. Write a Review on a Business(Restaurant)
	User should be able to post(write an review) on topic(business/restaurant).

	```java
	    @GetMapping("/write/review/businessId={business_id}&&stars={stars}&&text={reviewText}")
	    public String writeReview(@PathVariable String business_id, @PathVariable int stars,
	                              @PathVariable String reviewText) throws SQLException {
	        System.out.println("review text: "+reviewText);
	        if (user == null) {
	            return "Please register firstly. \n";
	        } else {
	            int code = user.writeReview(business_id, stars, reviewText, conn);
	            if (code == 1) {
	                return "Review written successfully. \n";
	            } else {
	                return "Please try again. \n";
	            }
	        }
	    }
	```

	```java
	    public int writeReview(String business_id, int stars, String review_text, Connection conn) throws SQLException {
	        int code = 0;
	        String review_id = generateUniqueId();
	
	        //get current date and time
	        LocalDateTime curTime = LocalDateTime.now();
	        DateTimeFormatter dateFormat = DateTimeFormatter.ofPattern("yyyy-MM-dd");
	        DateTimeFormatter timeFormat = DateTimeFormatter.ofPattern("HH:mm:ss");
	        String reviewDate = curTime.format(dateFormat);
	        String reviewTime = curTime.format(timeFormat);
	
	        // replace some text to avoid insert failure
	        review_text = review_text.replaceAll("\"", "");
	        review_text = review_text.replaceAll("\\\\", "/");
	        review_text = review_text.replaceAll(";", " ");
	
	        String sql = "INSERT INTO review (review_id, user_id, business_id, stars, reviewDate, reviewTime, reviewText) VALUES "
	                + "(\'" + review_id + "\',\'" + this.user_id + "\',\'" + business_id + "\',\'" + stars + "\',\'" + reviewDate + "\',\'" + reviewTime + "\',\"" + review_text + "\");";
	
	        System.out.println(sql);
	
	        try {
	            Boolean status = insertSQL(sql, conn);
	            if (!status) {
	                throw new SQLException("Can not write review, Please try again");
	            }
	
	            System.out.println("Review written successfully");
	            code = 1;
	        } catch (SQLException e) {
	            e.printStackTrace();
	            return code;
	        }
	        return code;
	
	    }
	```

	

15. Write a Tip on a Business(Restaurant)
	User should be able to write a tip on topic(business/restaurant).

	```java
	    @GetMapping("/write/tip/businessId={business_id}&&text={tipText}")
	    public String writeTip(@PathVariable String business_id, @PathVariable String tipText) throws SQLException {
	        if (user == null) {
	            return "Please register firstly. \n";
	        } else {
	            int code = user.writeTip(business_id, tipText, conn);
	            if (code == 1) {
	                return "Tip written successfully. \n";
	            } else {
	                return "Please try again. \n";
	            }
	        }
	    }
	```

	```java
	    public int writeTip(String business_id, String tipText, Connection conn) throws SQLException {
	        int code = 0;
	
	
	        //get current date and time
	        LocalDateTime curTime = LocalDateTime.now();
	        DateTimeFormatter dateFormat = DateTimeFormatter.ofPattern("yyyy-MM-dd");
	        DateTimeFormatter timeFormat = DateTimeFormatter.ofPattern("HH:mm:ss");
	        String postDate = curTime.format(dateFormat);
	        String postTime = curTime.format(timeFormat);
	
	        // replace some text to avoid insert failure
	        tipText = tipText.replaceAll("\"", "");
	        tipText = tipText.replaceAll("\\\\", "/");
	        tipText = tipText.replaceAll(";", " ");
	
	
	        String sql = "INSERT INTO tip (user_id, business_id, postDate, postTime, tipText) VALUES "
	                + "(\'" + this.user_id + "\',\'" + business_id + "\',\'" + postDate + "\',\'" + postTime + "\',\"" + tipText + "\");";
	        System.out.println(sql);
	        try {
	            Boolean status = insertSQL(sql, conn);
	            if (!status) {
	                throw new SQLException("Can not write tip, Please try again");
	            }
	
	            System.out.println("Tip written successfully");
	            code = 1;
	        } catch (SQLException e) {
	
	            e.printStackTrace();
	            return code;
	        }
	        
	        return code;
	    }
	```

	



**Testing**

Testing can be done by starting the server, and copy and paste the following urls to the browser.

By checking the return objects values, once could determine the result of the execution.



**Register**

```
curl -X POST "localhost:8080/register/test1";
```

Register successfully. Your userID is f7@N@@3QViWEpZL1Jtrla6



**Login**

```
curl -X GET "localhost:8080/login/___DPmKJsBF2X6ZKgAeGqg";
```

Login Successfully. Your UserID is: ___DPmKJsBF2X6ZKgAeGqg



**Refresh new reviews**

```
curl -X GET "localhost:8080/refresh/userId=QBDLNWKgldFPAfj8Z8F9Xg";
```

Before:

```mysql
mysql> select * from user_last_refresh;
Empty set (0.00 sec)
```

After:

```mysql
mysql> select * from user_last_refresh;
+------------------------+--------------+--------------+
| user_id                | refresh_time | refresh_date |
+------------------------+--------------+--------------+
| QBDLNWKgldFPAfj8Z8F9Xg | 14:15:23     | 2020-03-29   |
+------------------------+--------------+--------------+
1 row in set (0.00 sec)
```

Result:

![refresh_result](refresh_result.png)

Refresh again the returned result will be empty list(Since all read):

<img src="refresh_again.png" alt="refresh_again" style="zoom:50%;" />

**Make friend request**

```
curl -X GET "localhost:8080/addFriendRequest/__-Kt26YrtJxGdWs8FqKCg";
```

Friend request sent. 

```mysql
mysql> select * from friendrequest;
+------------------------+------------------------+
| user_id                | friend_id              |
+------------------------+------------------------+
| ___DPmKJsBF2X6ZKgAeGqg | __-Kt26YrtJxGdWs8FqKCg |
+------------------------+------------------------+
1 row in set (0.00 sec)

```



**Reject friend request**

```
curl -X GET "localhost:8080/rejectFriendRequest/___DPmKJsBF2X6ZKgAeGqg";
```

Friend request rejected

```mysql
mysql> select * from friendrequest;
Empty set (0.00 sec)
```



**Accept friend request**

```
curl -X GET "localhost:8080/acceptFriendRequest/___DPmKJsBF2X6ZKgAeGqg";
```

Accept friend request successfully.

```mysql
mysql> select * from friend where user_id = '__-Kt26YrtJxGdWs8FqKCg' and friend_id = '___DPmKJsBF2X6ZKgAeGqg';
+------------------------+------------------------+
| user_id                | friend_id              |
+------------------------+------------------------+
| __-Kt26YrtJxGdWs8FqKCg | ___DPmKJsBF2X6ZKgAeGqg |
+------------------------+------------------------+
1 row in set (0.00 sec)
```

```mysql
mysql> select * from friendrequest;
Empty set (0.00 sec)
```



**Vote(useful, funny, cool) review**

Before:

```mysql
mysql> select user_id, funny from user where user_id = "___DPmKJsBF2X6ZKgAeGqg";
```

```
+------------------------+-------+
| user_id                | funny |
+------------------------+-------+
| ___DPmKJsBF2X6ZKgAeGqg |     5 |
+------------------------+-------+
1 row in set (0.00 sec)
```

```mysql
mysql> select review_id, funny from review where review_id = "___-Bw8LtQgezPiN9xJWaQ";
+------------------------+-------+
| review_id              | funny |
+------------------------+-------+
| ___-Bw8LtQgezPiN9xJWaQ |     1 |
+------------------------+-------+
1 row in set (0.00 sec)
```



```
// type => 0: useful, 1: funny, 2: cool
curl -X GET "localhost:8080/vote/review_id=___-Bw8LtQgezPiN9xJWaQ&&type=1";
```

vote successfully. 

```mysql
mysql> select user_id, funny from user where user_id = "___DPmKJsBF2X6ZKgAeGqg";
+------------------------+-------+
| user_id                | funny |
+------------------------+-------+
| ___DPmKJsBF2X6ZKgAeGqg |     6 |
+------------------------+-------+
1 row in set (0.00 sec)
```

```mysql
mysql> select review_id, funny from review where review_id = "___-Bw8LtQgezPiN9xJWaQ";
+------------------------+-------+
| review_id              | funny |
+------------------------+-------+
| ___-Bw8LtQgezPiN9xJWaQ |     2 |
+------------------------+-------+
1 row in set (0.00 sec)
```



**Follow User**

Before

```mysql
mysql> select fans from user where user_id = "__-Kt26YrtJxGdWs8FqKCg";
+------+
| fans |
+------+
|    3 |
+------+
1 row in set (0.00 sec)
```

```
curl -i -X GET "localhost:8080/follow/user/__-Kt26YrtJxGdWs8FqKCg";
```

follow successfully. 

After:

```mysql
mysql> select fans from user where user_id = "__-Kt26YrtJxGdWs8FqKCg";
+------+
| fans |
+------+
|    4 |
+------+
1 row in set (0.00 sec)
```



**Choose Elite User**

Before:

```mysql
mysql> select * from eliteYear where user_id = "__-Kt26YrtJxGdWs8FqKCg";
Empty set (0.00 sec)
```

```
curl -i -X GET "localhost:8080/eliteuser/__-Kt26YrtJxGdWs8FqKCg";
```

Elect user as elite user this year successfully. 

After:

```mysql
mysql> select * from eliteYear where user_id = "__-Kt26YrtJxGdWs8FqKCg";
+------------------------+-----------+
| user_id                | eliteYear |
+------------------------+-----------+
| __-Kt26YrtJxGdWs8FqKCg |      2020 |
+------------------------+-----------+
1 row in set (0.00 sec)
```



**Reply Review**

```
//Login First
http://localhost:8080/login/QBDLNWKgldFPAfj8Z8F9Xg
//Reply to specific review given review_id
http://localhost:8080/reply/review/businessId=5z1WIr7E9P2CSzyN5seeSA&&stars=5&&text=awesome&&responseTo=Y3pR0ZXAtxoROZ2NBE_CGQ

```

<img src="replydone.png" alt="replydone" style="zoom:50%;" />

New review is generated:

```mysql
mysql> select review_id,reviewText from review where review_id = "3iL+xGMHxze^Ju+8D64gUJ";
+------------------------+------------+
| review_id              | reviewText |
+------------------------+------------+
| 3iL+xGMHxze^Ju+8D64gUJ | awesome    |
+------------------------+------------+
1 row in set (0.00 sec)

```

Relationship between reviews are also stored:

```mysql
mysql> select * from reviewRelation;
+------------------------+------------------------+
| review_id              | response_to_review_id  |
+------------------------+------------------------+
| 3iL+xGMHxze^Ju+8D64gUJ | Y3pR0ZXAtxoROZ2NBE_CGQ |
| Zz-HU-5DUJXfBv6zZA-9!K | Y3pR0ZXAtxoROZ2NBE_CGQ |
+------------------------+------------------------+
2 rows in set (0.00 sec)
```



**Upvote a Tip**

```
//hot:0, more:1, profile:2, cute:3, list:4, note:5, plain:6, cool:7, funny:8, writer:9, 
//photos:10

http://localhost:8080/compliment/tip/tipID=1&&compliment=3
```

Before:

```mysql
mysql> select user_id,compliment_cute from user where user_id =  'UPw5DWs_b-e2JRBS-t37Ag';
+------------------------+-----------------+
| user_id                | compliment_cute |
+------------------------+-----------------+
| UPw5DWs_b-e2JRBS-t37Ag |               0 |
+------------------------+-----------------+
1 row in set (0.00 sec)

mysql> select tip_id,compliment_count from tip where tip_id =1;
+--------+------------------+
| tip_id | compliment_count |
+--------+------------------+
|      1 |                0 |
+--------+------------------+
1 row in set (0.00 sec)
```

<img src="upvoteTip.png" alt="upvoteTip" style="zoom:50%;" />

After:

```mysql
mysql> select user_id,compliment_cute from user where user_id =  'UPw5DWs_b-e2JRBS-t37Ag';
+------------------------+-----------------+
| user_id                | compliment_cute |
+------------------------+-----------------+
| UPw5DWs_b-e2JRBS-t37Ag |               1 |
+------------------------+-----------------+
1 row in set (0.00 sec)

mysql> select tip_id,compliment_count from tip where tip_id =1;
+--------+------------------+
| tip_id | compliment_count |
+--------+------------------+
|      1 |                1 |
+--------+------------------+
1 row in set (0.00 sec)
```



**Create a Group**

```
curl -i -X POST -H "Content-type: application/json" -d '{"groupName": "abc", "friends": ["___DPmKJsBF2X6ZKgAeGqg", "___fEWlObjtPaZ-pK0eq9g"]}' localhost:8080/creategroup;
```

```
Content-Type: text/plain;charset=UTF-8
Content-Length: 28
Date: Sat, 04 Apr 2020 20:23:58 GMT

create group successfully.
```

Result:

```mysql
mysql> select * from group_info;
+------------------------+------+
| group_id               | name |
+------------------------+------+
| Qyu0kYYcZ6sla0-HBcYV1z | abc  |
+------------------------+------+
1 row in set (0.00 sec)
```

```mysql
mysql> select * from user_group;
+------------------------+------------------------+
| group_id               | user_id                |
+------------------------+------------------------+
| Qyu0kYYcZ6sla0-HBcYV1z | ___DPmKJsBF2X6ZKgAeGqg |
| Qyu0kYYcZ6sla0-HBcYV1z | ___fEWlObjtPaZ-pK0eq9g |
| Qyu0kYYcZ6sla0-HBcYV1z | QBDLNWKgldFPAfj8Z8F9Xg |
+------------------------+------------------------+
3 rows in set (0.00 sec)
```



**Join an existing group**

```
http://localhost:8080/login/___QCazm0YrHLd3uNUPYMA
http://localhost:8080/join/group/groupID='Qyu0kYYcZ6sla0-HBcYV1z'
```

Before:

```mysql
mysql> select * from user_group;
+------------------------+------------------------+
| group_id               | user_id                |
+------------------------+------------------------+
| Qyu0kYYcZ6sla0-HBcYV1z | ___DPmKJsBF2X6ZKgAeGqg |
| Qyu0kYYcZ6sla0-HBcYV1z | ___fEWlObjtPaZ-pK0eq9g |
| Qyu0kYYcZ6sla0-HBcYV1z | QBDLNWKgldFPAfj8Z8F9Xg |
+------------------------+------------------------+
3 rows in set (0.00 sec)
```

After:

```
mysql> select * from user_group;
+------------------------+------------------------+
| group_id               | user_id                |
+------------------------+------------------------+
| Qyu0kYYcZ6sla0-HBcYV1z | ___DPmKJsBF2X6ZKgAeGqg |
| Qyu0kYYcZ6sla0-HBcYV1z | ___fEWlObjtPaZ-pK0eq9g |
| Qyu0kYYcZ6sla0-HBcYV1z | ___QCazm0YrHLd3uNUPYMA |
| Qyu0kYYcZ6sla0-HBcYV1z | QBDLNWKgldFPAfj8Z8F9Xg |
+------------------------+------------------------+
4 rows in set (0.00 sec)
```



**Follow a Business(Restaurant)**

```
http://localhost:8080/follow/restaurant/businessId='__1uG7MLxWGFIv2fCGPiQQ'
```

Before:

```mysql
mysql> select * from user_follow_business;
Empty set (0.00 sec)
```

<img src="followBusiness.png" alt="followBusiness" style="zoom:50%;" />

After:

```mysql
mysql> select * from user_follow_business;
+------------------------+------------------------+
| user_id                | business_id            |
+------------------------+------------------------+
| QBDLNWKgldFPAfj8Z8F9Xg | __1uG7MLxWGFIv2fCGPiQQ |
+------------------------+------------------------+
1 row in set (0.00 sec)
```



**Write a Review on a Business(Restaurant)**

```
http://localhost:8080/write/review/businessId=__1uG7MLxWGFIv2fCGPiQQ&&stars=5&&text="very good food"
```

<img src="writeReivew.png" alt="writeReivew" style="zoom:50%;" />

Before:

```mysql
mysql> select review_id from review where user_id = 'QBDLNWKgldFPAfj8Z8F9Xg';
+------------------------+
| review_id              |
+------------------------+
| 3iL+xGMHxze^Ju+8D64gUJ |
| cQ-mvJZ9zneSYn7m0b2FAA |
| Zz-HU-5DUJXfBv6zZA-9!K |
+------------------------+
3 rows in set (0.00 sec)
```

After:

```mysql
mysql> select review_id from review where user_id = 'QBDLNWKgldFPAfj8Z8F9Xg';
+------------------------+
| review_id              |
+------------------------+
| 3iL+xGMHxze^Ju+8D64gUJ |
| cQ-mvJZ9zneSYn7m0b2FAA |
| FkNuOEzRdcPSKU3p-o@9M+ |
| Zz-HU-5DUJXfBv6zZA-9!K |
+------------------------+
4 rows in set (0.00 sec)

mysql> select * from review where review_id = 'FkNuOEzRdcPSKU3p-o@9M+';
+------------------------+------------------------+------------------------+-------+------------+------------+----------------+--------+-------+------+
| review_id              | user_id                | business_id            | stars | reviewDate | reviewTime | reviewText     | useful | funny | cool |
+------------------------+------------------------+------------------------+-------+------------+------------+----------------+--------+-------+------+
| FkNuOEzRdcPSKU3p-o@9M+ | QBDLNWKgldFPAfj8Z8F9Xg | __1uG7MLxWGFIv2fCGPiQQ |     5 | 2020-03-30 | 12:33:46   | very good food |      0 |     0 |    0 |
+------------------------+------------------------+------------------------+-------+------------+------------+----------------+--------+-------+------+
1 row in set (0.00 sec)
```



**Write a Tip on a Business(Restaurant)**

```
http://localhost:8080/write/tip/businessId=__1uG7MLxWGFIv2fCGPiQQ&&text="must try the hidden menu!"
```

<img src="writeTip.png" alt="writeTip" style="zoom:50%;" />

Before:

```mysql
mysql> select * from tip where user_id = 'QBDLNWKgldFPAfj8Z8F9Xg';
Empty set (0.01 sec)

```

After:

```mysql
mysql> select * from tip where user_id = 'QBDLNWKgldFPAfj8Z8F9Xg';
+---------+------------------------+------------------------+---------------------------+------------+----------+------------------+
| tip_id  | business_id            | user_id                | tipText                   | postDate   | postTime | compliment_count |
+---------+------------------------+------------------------+---------------------------+------------+----------+------------------+
| 1223095 | __1uG7MLxWGFIv2fCGPiQQ | QBDLNWKgldFPAfj8Z8F9Xg | must try the hidden menu! | 2020-03-30 | 12:41:55 |                0 |
+---------+------------------------+------------------------+---------------------------+------------+----------+------------------+
1 row in set (0.00 sec)
```

