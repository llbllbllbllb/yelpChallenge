package com.ece656.ece656spring.controllers;


import com.ece656.ece656spring.business.user;
import com.ece656.ece656spring.database.dbConnection;
import com.ece656.ece656spring.model.CreateGroupBean;
import org.springframework.web.bind.annotation.*;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Map;

@RestController
public class controller {
    dbConnection dbConnection = new dbConnection();
    Connection conn = dbConnection.connectDB();
    private user user;
    @GetMapping("/hello")
    public String getHelloMessage() {
        return "Hello world!\n";
    }

//    @GetMapping("/register")
//    public user register() {
//        user user = new user("tony");
//        return user;
//    }

    @PostMapping("/register/{name}")
    public user register(@PathVariable String name) {
        user = new user(name);
        int code = user.newUser(conn);
        if (code == 1) {
            return user;
        } else {
            return new user();
        }
    }

    @GetMapping("/addFriendReauest/{friendRequest_id}")
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

//     0: useful, 1: funny, 2: cool
    @GetMapping("/vote?review_id={review_id}&&type={i}")
    public String vote(@PathVariable String review_id, @PathVariable int i) throws SQLException {
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

    @GetMapping("/follow/user?{user_id}")
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

    @GetMapping("/reply/review?businessId={business_id}&&stars={stars}&&text={reviewText}&&responseTo={response_to_review_id}")
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

    //    hot:0, more:1, profile:2, cute:3, list:4, note:5, plain:6, cool:7, funny:8, writer:9, photos:10
    @GetMapping("/compliment/tip?tipID={tip_id}&&compliment={i}")
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

    @GetMapping("/join/group?groupID={group_id}")
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

    @GetMapping("/follow/restaurant?businessID={business_id}")
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

    @GetMapping("/write/review?businessId={business_id}&&stars={stars}&&text={reviewText}")
    public String writeReview(@PathVariable String business_id, @PathVariable int stars,
                              @PathVariable String reviewText) throws SQLException {
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

    @GetMapping("/write/tip?businessId={business_id}&&text={tipText}")
    public String writeReview(@PathVariable String business_id, @PathVariable String tipText) throws SQLException {
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



}
