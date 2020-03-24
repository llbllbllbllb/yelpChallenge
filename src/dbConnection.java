import java.sql.*;

public class dbConnection {
    public Connection connectDB(){
        try{
            String driverName = "com.mysql.cj.jdbc.Driver";
            Class.forName(driverName); // here is the ClassNotFoundException

            String serverName = "localhost";
            String mydatabase = "yelp";
            String url = "jdbc:mysql://" + serverName + "/" + mydatabase + "?serverTimezone=UTC";

            String username = "root";
            String password = "mysql";
            Connection conn = DriverManager.getConnection(url, username, password);
            return  conn;

        }catch(Exception e){
            e.printStackTrace();
            System.out.println("Error: Cannot connect DB...");
        }
        return null;

    }

    public void closeConnection(Connection conn){
        try{
            conn.close();
        }catch (Exception e){
            System.out.println("Cannot close connection...");
        }
    }

    public ResultSet executeSQL(String sql, Connection conn){
        Statement stmt = null;
        try{
            stmt = conn.createStatement();
            return stmt.executeQuery(sql);
        }catch (Exception e){
            System.out.println("Unable to execute sql statement...");
        }
        return null;

    }

    public boolean insertSQL(String sql, Connection conn){
        Statement stmt = null;
        try{
            stmt = conn.createStatement();
            stmt.executeUpdate(sql);
            return true;
        }catch (Exception e){
            e.printStackTrace();
            System.out.println("Unable to execute sql statement...");
            return false;
        }
    }
}
