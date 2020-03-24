import java.sql.*;
import java.time.Year;
import java.util.ArrayList;
import java.time.LocalDate;
import java.util.Random;

public class user extends dbConnection{
    private String AlphaNumericString = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            + "0123456789"
            + "abcdefghijklmnopqrstuvxyz"
            + "-_!@#$%^&+=";
    private String user_id;
    private String user_name;
    private LocalDate yelping_since;
//    private int last_refresh_time;

    public user(){}

    public user(String user_name) {
        this.user_id = generateUniqueId();
        this.user_name = user_name;
        this.yelping_since = LocalDate.now();
    }

    public String generateUniqueId() {
        int n = 22;
        StringBuilder sb = new StringBuilder(22);
        for (int i = 0; i < n; i++ ) {
            int index = (int)(AlphaNumericString.length() * Math.random());
            sb.append(AlphaNumericString.charAt(index));
        }
        return sb.toString();
    }

    public String getUser_id() {
        return user_id;
    }

    public void setUser_id(String user_id) {
        this.user_id = user_id;
    }

    public String getUser_name() {
        return user_name;
    }

    public void setUser_name(String user_name) {
        this.user_name = user_name;
    }

    public LocalDate getYelping_since() {
        return yelping_since;
    }

    public void setYelping_since(LocalDate yelping_since) {
        this.yelping_since = yelping_since;
    }

    //    public int getLast_refresh_time() {
//        return last_refresh_time;
//    }
//
//    public void setLast_refresh_time(int last_refresh_time) {
//        this.last_refresh_time = last_refresh_time;
//    }


    public void newUser(Connection conn){

        String sql = "INSERT INTO user (user_id, name, yelping_since) " +
                "VALUES (" + "\"" + this.user_id + "\", \"" + this.user_name + "\" ,\""  + this.yelping_since + "\");";
        System.out.println(sql);
        boolean status = insertSQL(sql, conn);
        if (status == true) {
            System.out.println("Registration successfully!");
        } else {
            System.out.println("Please try again");
        }
    }

    public void confirmAddFriend(String friend_id, Connection conn) {
        String sql = "INSERT INTO friend (user_id, friend_id) " +
                "VALUES (" + "\"" + this.user_id + "\", \"" + friend_id + "\");";
        System.out.println(sql);
        Boolean status = insertSQL(sql, conn);
        if (status == true) {
            System.out.println("Added friend successfully!");
        } else {
            System.out.println("Please try again");
        }
    }

//    votes sent by the user 0: useful, 1: funny, 2: cool
    public void vote(String review_id, int i, Connection conn) throws SQLException {
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
                    "IF ("+ type +" is null, 1, "+ type + " + 1) WHERE user_id = \"" + this.user_id + "\";";
            String query2 = "UPDATE review SET " + type + " = " +
                    "IF (" + type + " is null, 1, "+ type +" + 1) WHERE review_id = \"" + review_id + "\";";
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
            } catch (SQLException e) {
                conn.rollback();
                e.printStackTrace();
            } finally {
                conn.setAutoCommit(true);
            }
        }
    }

    public void complimentTip(String tip_id, Connection connection) throws SQLException {
        String query = "UPDATE tip SET compliment_count = compliment_count + 1 where tip_id = \'" + tip_id + "\';";
        try {
            conn.setAutoCommit(false);
            Boolean status = insertSQL(query, conn);
            if (!status) {
                throw new SQLException("Please try again");
            }
            conn.commit();
            System.out.println("upvote tip successfully");
        } catch (SQLException e) {
            conn.rollback();
            e.printStackTrace();
        } finally {
            conn.setAutoCommit(true);
        }
    }

    //    fan table???
    public void followUser(String user_id, Connection conn) {
        String sql = "UPDATE user SET fans = " +
                "IF (fans is null, 1, fans + 1) WHERE user_id = \"" + user_id + "\";";
        Boolean status = insertSQL(sql, conn);
        if (status == true) {
            System.out.println("follow successfully");
        } else {
            System.out.println("Please try again");
        }
    }

    public void eliteUser(String user_id, Connection conn) {
        int currentYear = Year.now().getValue();
        String sql = "INSERT INTO eliteYear VALUES(\"" + user_id + "\", \"" + currentYear + "\");";
        System.out.println(sql);

        Boolean status = insertSQL(sql, conn);
        if (status == true) {
            System.out.println("Elect user successfully");
        } else {
            System.out.println("Please try again");
        }
    }

//    not sure about compliment ???
//    hot:0, more:1, profile:2, cute:3, list:4, note:5, plain:6, cool:7, funny:8, writer:9, photos:10
    public void complimentUser(int i, Connection conn) {
        String user = "0T8Nted2-45Q47vX7S7=2X";
        String compliment = null;
        String[] compliments = {"compliment_hot", "compliment_more", "compliment_profile", "compliment_cute", "compliment_list", "compliment_note", "compliment_plain", "compliment_cool", "compliment_funny",         "compliment_writer", "compliment_photos"};
        if (i >= 0 && i <= 10 ) {
            compliment = compliments[i];
        }
        if (compliment != null) {
            String query = "UPDATE user SET " + compliment + " = " +
                    "IF (" + compliment + " is null, 1, " + compliment + " + 1) WHERE user_id = \"" + user + "\";";
            System.out.println(query);
            Boolean status = insertSQL(query, conn);
            if (status == true) {
                System.out.println("successfully");
            } else {
                System.out.println("Please try again");
            }
        }
    }

    public void createGroup(String groupname, Connection conn) {
        if(groupname == null || groupname.length() == 0) {
            System.out.println("Error: Empty group name.");
            return;
        }

        String group_id = generateUniqueId();

        sql = "INSERT INTO group_info (group_id,name) VALUES (\'"+group_id+"\',\'"+groupname+"\');";
        sql2 = "INSERT INTO user_group (group_id,user_id) VALUES (\'"+group_id+"\',\'"+this.user_id+"\');";

        try {
            conn.setAutoCommit(false);
            Boolean status = insertSQL(sql, conn);
            Boolean status2 = insertSQL(sql2, conn);
            if (!status || !status2) {
                throw new SQLException("Please try again");
            }
            conn.commit();
            System.out.println("create group successfully");
        } catch (SQLException e) {
            conn.rollback();
            e.printStackTrace();
        } finally {
            conn.setAutoCommit(true);
        }

    }




//
//
//    public void newPost(String txt, ArrayList<String> Images, ArrayList<String> Links, String topic, Connection conn) throws SQLException {
//        long unixTime = System.currentTimeMillis() / 1000L;
//
//        // text
//        String sql = "INSERT INTO Post (user_id,text,time) VALUES (" + this.user_id + ", \"" + txt + "\" , " + unixTime + ");";
//        System.out.println(sql);
//        insertSQL(sql, conn);
//
//        // get post_id
//        sql = "SELECT post_id FROM Post WHERE user_id = " + this.user_id + " ORDER BY post_id DESC LIMIT 1;";
//        System.out.println(sql);
//        ResultSet rs = executeSQL(sql,conn);
//        String post_id = "";
//        while(rs.next()){
//            post_id = rs.getString("post_id");
//        }
//        System.out.println("post_id: "+post_id);
//
//        // images
//        if(Images != null) {
//            for (int i = 0; i < Images.size(); i++) {
//                String image_url = Images.get(i);
//                sql = "INSERT INTO PostImage (post_id,image_url) VALUES (" + post_id + ", \"" + image_url + "\");";
//                System.out.println(sql);
//                insertSQL(sql, conn);
//            }
//        }
//
//        // links
//        if(Links != null) {
//            for (int i = 0; i < Links.size(); i++) {
//                String link_url = Links.get(i);
//                sql = "INSERT INTO PostLink (post_id,link_url) VALUES (" + post_id + ", \"" + link_url + "\");";
//                System.out.println(sql);
//                insertSQL(sql, conn);
//            }
//        }
//
//        // topic
//        if (topic != null || topic.length() > 0) {
//            topic = topic.toLowerCase();
//            // first check if topic exist in Topics table:
//            sql = "SELECT topic_id FROM Topics WHERE topic_name = \"" + topic +"\";";
//            rs = executeSQL(sql,conn);
//
//            if(!rs.isBeforeFirst() ) {
//                // create topic
//                System.out.println(topic + " is not in Topics table, creating new topic...");
//                sql = "INSERT INTO Topics (topic_name,creator_id) VALUES (\"" + topic + "\", " + this.user_id + ");";
//                insertSQL(sql,conn);
//                System.out.println("Topic created...");
//                // now need to get user-created topic_id:
//                System.out.println("Fetching topic id...");
//                sql = "SELECT topic_id FROM Topics WHERE creator_id = " + this.user_id + " ORDER BY topic_id DESC LIMIT 1;";
//                rs = executeSQL(sql,conn);
//                String topic_id = "";
//                while(rs.next()){
//                    topic_id = rs.getString("topic_id");
//                }
//                System.out.println("topic_id: "+topic_id);
//                // build the post-topic relation:
//                System.out.println("Building Post-Topic Relation...");
//                sql = "INSERT INTO PostTopics (post_id,topic_id) VALUES (" + post_id + ", " + topic_id + ");";
//                insertSQL(sql,conn);
//                System.out.println("Relation Built...");
//            }
//            else {
//                String topic_id = "";
//                while(rs.next()){
//                    topic_id = rs.getString("topic_id");
//                }
//                System.out.println(topic + " is already in Topics table with topic_id = " + topic_id + "...");
//                // build the post-topic relation:
//                System.out.println("Building Post-Topic Relation...");
//                sql = "INSERT INTO PostTopics (post_id,topic_id) VALUES (" + post_id + ", " + topic_id + ");";
//                insertSQL(sql,conn);
//                System.out.println("Relation Built...");
//
//            }
//        }
//
//
//
//
//    }
//
//    public void followUser(int user_id_ToFollow, Connection conn) throws SQLException{
//        //first check if already following
//        String sql = "SELECT user_id,friend_id FROM Friend WHERE user_id = " + this.user_id +" and friend_id = " + user_id_ToFollow +";";
//        ResultSet rs = executeSQL(sql,conn);
//        if(!rs.isBeforeFirst() ){
//            // not exist, add friend relation
//            System.out.println("Relation not found, following: ");
//            sql = "insert into Friend (user_id,friend_id) values ("+ this.user_id +", " + user_id_ToFollow + ");";
//            insertSQL(sql,conn);
//            System.out.println(Integer.toString(this.user_id)+" is following "+Integer.toString(user_id_ToFollow)+" now...");
//        }
//        else{
//            // exist, do nothing
//            System.out.println("Already following " + Integer.toString(user_id_ToFollow));
//        }
//
//
//    }
//
//    public void followTopic(String topic_name, Connection conn) throws  SQLException{
//        topic_name = topic_name.toLowerCase();
//        // check if topic exist
//        String sql = "SELECT topic_id FROM Topics WHERE topic_name = \"" + topic_name +"\";";
//        ResultSet rs = executeSQL(sql,conn);
//        if(!rs.isBeforeFirst() ) {
//            // create topic
//            System.out.println(topic_name + " is not in Topics table, creating new topic...");
//            sql = "INSERT INTO Topics (topic_name,creator_id) VALUES (\"" + topic_name + "\", " + this.user_id + ");";
//            insertSQL(sql, conn);
//            System.out.println("Topic created...");
//            // now need to get user-created topic_id:
//            System.out.println("Fetching topic id...");
//            sql = "SELECT topic_id FROM Topics WHERE creator_id = " + this.user_id + " ORDER BY topic_id DESC LIMIT 1";
//            rs = executeSQL(sql, conn);
//            String topic_id = "";
//            while (rs.next()) {
//                topic_id = rs.getString("topic_id");
//            }
//            System.out.println("topic_id: " + topic_id);
//            // user now can follow the topic
//            System.out.println("User following topic...");
//            sql = "INSERT INTO UserFollowTopics (user_id,topic_id) VALUES (" + this.user_id + ", " + topic_id  + ");";
//            insertSQL(sql,conn);
//            System.out.println("User has followed \"" + topic_name +"\"");
//        }
//        else{
//            // get topic_id
//            String topic_id = "";
//            while(rs.next()){
//                topic_id = rs.getString("topic_id");
//            }
//            // check if already follow
//            sql = "SELECT topic_id FROM UserFollowTopics WHERE user_id = " + this.user_id +" and topic_id = " + topic_id + ";";
//            rs = executeSQL(sql,conn);
//            if(!rs.isBeforeFirst()){
//                // not follow
//                System.out.println("User following topic...");
//                sql = "INSERT INTO UserFollowTopics (user_id,topic_id) VALUES (" + this.user_id + ", " + topic_id  + ");";
//                insertSQL(sql,conn);
//                System.out.println("User has followed \"" + topic_name +"\"");
//            }
//            else{
//                // already followed
//                System.out.println("User has already followed topic \"" + topic_name +"\"");
//            }
//        }
//
//    }
//
//    public void responsePost(Connection conn, int post_id, String text) throws  SQLException {
//        if (text == null || text.length() == 0) {
//            text = "Repost";
//        }
////        check responded post is responded post itself
//        String sql = "SELECT * FROM PostRelation WHERE post_id = " + post_id + ";";
//        ResultSet rs = executeSQL(sql,conn);
//        String  user_name;
//        String originText;
//        String topic_name = null;
//        int newPostId = 0;
//        boolean isOriginal = true;
//
////
//        if (rs.isBeforeFirst()){
//            isOriginal = false;
//            System.out.println("Original Post is Not a YuanChuang");
//            sql = "SELECT A.user_name, A.text, B.topic_name " +
//                    " FROM " +
//                    " (SELECT user_name, text, post_id " +
//                    " FROM Post, user WHERE Post.post_id = " + post_id +
//                    " and Post.user_id = user.user_id) A " +
//                    " LEFT OUTER JOIN " +
//                    " (SELECT topic_name,post_id " +
//                    " from PostTopics,Topics " +
//                    " where PostTopics.post_id = " + post_id +" ) B " +
//                    " ON A.post_id = B.post_id;";
//            System.out.println(sql);
//            rs = executeSQL(sql, conn);
//            while (rs.next()) {
//                user_name = rs.getString("user_name");
//                originText = rs.getString("text");
//                topic_name = rs.getString("topic_name");
//                text += "//@" + user_name + ":" + originText;
//            }
//        } else {
//            sql = "SELECT topic_name,post_id " +
//                    "from PostTopics,Topics " +
//                    "where PostTopics.post_id = " + post_id + ";";
//            rs = executeSQL(sql,conn);
//            while(rs.next()){
//                topic_name = rs.getString("topic_name");
//            }
//            System.out.println("Original Post is YuanChuang");
//        }
//        System.out.println(topic_name);
////        response to certain post_id
//        this.newPost(text, null, null, topic_name, conn);
//
////        get post_id
//        sql = "SELECT post_id FROM Post WHERE user_id = " + this.user_id + " ORDER BY post_id DESC LIMIT 1;";
//        System.out.println("Hahaha");
//        System.out.println(sql);
//        rs = executeSQL(sql, conn);
//        while (rs.next()) {
//            newPostId = rs.getInt("post_id");
//        }
//        System.out.println("newPostId: "+newPostId);
////        set PostRelation
//        int origin_post_id = post_id;
//        if(!isOriginal) {
//            sql = "select response_to_post from PostRelation where post_id =" + post_id + ";";
//            System.out.println(sql);
//            rs = executeSQL(sql,conn);
//            while(rs.next()){
//                origin_post_id = rs.getInt("response_to_post");
//            }
//        }
//        sql = "INSERT INTO PostRelation (post_id, response_to_post) values (" + newPostId + "," + origin_post_id + ");";
//
//        if (newPostId != 0) {
//            insertSQL(sql, conn);
//        }
//    }
//
//    public void thumbUpPost(Connection conn, int post_id) throws SQLException {
////        check if the post exists
//        String sql = "SELECT post_id FROM Post WHERE post_id = " + post_id + ";";
//        ResultSet rs = executeSQL(sql, conn);
//        if (rs.isBeforeFirst()) {
//            System.out.println("post exist");
//            sql = "select * from ThumbsUp WHERE post_id =  " + post_id + " and user_id = " + this.user_id + ";";
//            rs = executeSQL(sql, conn);
//            if(!rs.isBeforeFirst()) {
//                // delete up vote if exist
//                sql = "select * from ThumbsDown WHERE post_id =  " + post_id + " and user_id = " + this.user_id + ";";
//                rs = executeSQL(sql,conn);
//                if(rs.isBeforeFirst()){
//                    System.out.println("You down voted this post, cancelling it...");
//                    sql = "delete from ThumbsDown where post_id = " + post_id +" and user_id = " + this.user_id +";";
//                    insertSQL(sql,conn);
//                }
//                // inset down vote
//                sql = "INSERT INTO ThumbsUp(post_id, user_id) VALUES (" + post_id + ", " + this.user_id + ");";
//                insertSQL(sql, conn);
//                System.out.println("thumb up to post successfully");
//            }
//            else{
//                System.out.println("You have already Up vote this post...");
//            }
//        }
//    }
//
//    public void thumbDownPost(Connection conn, int post_id) throws SQLException {
////        check if the post exists
//        String sql = "SELECT post_id FROM Post WHERE post_id = " + post_id + ";";
//        ResultSet rs = executeSQL(sql, conn);
//        if (rs.isBeforeFirst()) {
//            System.out.println("post exist");
//            sql = "select * from ThumbsDown WHERE post_id =  " + post_id + " and user_id = " + this.user_id + ";";
//            rs = executeSQL(sql, conn);
//            if(!rs.isBeforeFirst()) {
//                // delete up vote if exist
//                sql = "select * from ThumbsUp WHERE post_id =  " + post_id + " and user_id = " + this.user_id + ";";
//                rs = executeSQL(sql,conn);
//                if(rs.isBeforeFirst()){
//                    System.out.println("You up voted this post, cancelling it...");
//                    sql = "delete from ThumbsUp where post_id = " + post_id +" and user_id = " + this.user_id +";";
//                    insertSQL(sql,conn);
//                }
//                // inset down vote
//                sql = "INSERT INTO ThumbsDown(post_id, user_id) VALUES (" + post_id + ", " + this.user_id + ");";
//                insertSQL(sql, conn);
//                System.out.println("thumb down to post successfully");
//            }
//            else{
//                System.out.println("You have already Down vote this post...");
//            }
//        }
//    }
//
//
//    public void refreshPost(Connection conn) throws SQLException{
//
//        int lastRefreshTime = 0;
//        String sql = "select last_refresh_time from User where user_id = " + this.user_id + ";";
//        ResultSet rs = executeSQL(sql,conn);
//        while(rs.next()){
//            lastRefreshTime = rs.getInt("last_refresh_time");
//        }
//        System.out.println("Last refresh time: "+lastRefreshTime);
//
//        // Refresh from friends and topics and order by time DESC
//        sql =   "select PostInfo.time as time, PostInfo.post_id as post_id, PostInfo.text as text, OriginText.text as OriginPost from \n" +
//                "(select * from Post where\n"+
//                "(user_id in\n"+
//                "(select friend_id as user_id from Friend where user_id = "+this.user_id+") and time >"+lastRefreshTime+") \n"+
//                "or\n"+
//                "(post_id in\n"+
//                "(select post_id from \n"+
//                "(select * from PostTopics) A\n"+
//                "inner join\n"+
//                "(select topic_id from UserFollowTopics where user_id = "+this.user_id+") B\n"+
//                "on A.topic_id = B.topic_id) and time >"+lastRefreshTime+")\n"+
//                "order by time DESC ) PostInfo\n" +
//                "left join\n" +
//                "(select PostRelation.post_id,response_to_post,text from PostRelation,Post where PostRelation.response_to_post = Post.post_id) OriginText\n" +
//                " on  OriginText.post_id = PostInfo.post_id;";
////        System.out.println(sql);
//        rs = executeSQL(sql,conn);
//        while(rs.next()){
//            int time = rs.getInt("time");
//            Date date= new Date(time * 1000L);
//            System.out.println(date);
//            System.out.println(rs.getString("post_id"));
//            System.out.println(rs.getString("text"));
//            if(rs.getString("OriginPost") != null){
//                System.out.println("\t|-"+rs.getString("OriginPost"));
//            }
//
//        }
//
////        update time
//        int unixTime = (int) (System.currentTimeMillis() / 1000L);
//        sql = "UPDATE User SET last_refresh_time  = " + unixTime + " WHERE user_id = " + this.user_id + ";";
//        insertSQL(sql, conn);
//    }
}
