package com.ece656.ece656spring.model;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.List;

public class CreateGroupBean {
    private String groupName;
    private ArrayList<String> friends;

    public CreateGroupBean() {
    }

    public CreateGroupBean(String groupName, ArrayList<String> friends) {
        this.groupName = groupName;
        this.friends = friends;
    }

    public String getGroupName() {
        return groupName;
    }

    public void setGroupName(String groupName) {
        this.groupName = groupName;
    }

    public ArrayList<String> getFriends() {
        return friends;
    }

    public void setFriends(ArrayList<String> friends) {
        this.friends = friends;
    }
}
