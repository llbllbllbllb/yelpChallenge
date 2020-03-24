import java.sql.*;
import java.util.ArrayList;


public class mainProgram {

    public static void main(String[] args){
        try{
            dbConnection dbConnection = new dbConnection();
            Connection conn = dbConnection.connectDB();
            user tony = new user("tony");
//            tony.newUser(conn);
//            tony.addFriend("94rYTkXsdqESRHnBf1UldA", conn);
//            tony.vote("123", 1, conn);
//            tony.eliteUser("94rYTkXsdqESRHnBf1UldA", conn);
            tony.complimentUser(5, conn);
//            User ivan = new User(295319725,"llb",'M');
//
//            ivan.refreshPost(conn);
//
//            User tony = new User(123456789,"z299lin", 'M');
//
//            tony.newUser(conn);
//
//            tony.followTopic("sport", conn);
//
//            ivan.newUser(conn);
//
//            ivan.followTopic("sports",conn);
//
//            ArrayList<String> images = new ArrayList<String>();
//            images.add("image 1");
//            images.add("image 2");
//            ArrayList<String> links = new ArrayList<String>();
//            links.add("link 1");
//            links.add("link 2");
//
//            String topic = "Food";
//
//            ivan.newPost("hello world2",images,links,topic, conn);
//
//            ivan.followUser(tony.getUser_id(),conn);
//
//            String sql = "select user_id from User limit 3;";
//            ResultSet rs = dbConnection.executeSQL(sql,conn);
//
//            while(rs.next()){
//                // 通过字段检索
//                int id  = rs.getInt("user_id");
//
//                // 输出数据
//                System.out.print("ID: " + id);
//                System.out.print("\n");
//            }
            dbConnection.closeConnection(conn);

        }catch(Exception e){
            System.out.println(e.toString());
        }
    }
}
