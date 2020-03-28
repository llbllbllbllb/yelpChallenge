# **ECE656 Project Report: A Simple Social Network (with Yelp Dataset)**

Student Name: Libang Liang, Student ID: 20662701

Student Name: Zhiming Lin, Student ID:



#### 1. ER Model

#### 2. Create Tables

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





#### 4. Client(README)

We created set of APIs using Java with Spring Boot Framwork. User can do the following functions:

1. Register
   User should be able to register a new user account by providing a user name, a unique user id is created and returned to the user.

2. Login
   User should be able to login ther account by providing their user id.

3. Refresh new reviews if they followed any business(restaurant) or friends
   User should be able to look at their unseen reviews based on the 1. business(restaurant) they followed, 2. freinds they have.

4. Make friend request

   User should be able to make friend request if they can provide friend's user id.
   

5. Accept/Reject friend request
   User should be able to accept or reject any pending friend request.

6. Vote(useful, funny, cool) review
   User should be able to vote reviews if they can provide the review id and the type of vote.

7. Follow User
   User should be able to follow user.

8. Choose Elite User
   User could be chosen to be elite user for specific year.

9. Reply Review
   User should be able to reply a review if they can provide the original review id.

   

10. Upvote a Tip
    User should be able to upvote a tip if they can provide tip id.

11. Create a Group
    User should be able to create a group if they can provide list of user id(s).

12. Join an existing group
    User should be able to join an existing group if they can provide a group id.

13. Follow a Business(Restaurant)
    User should be able to follow a business(restaurant) if they can provide the business id.

14. Write a Review on a Business(Restaurant)
    User should be able to post(write an review) on topic(business/restaurant).

15. Write a Tip on a Business(Restaurant)
    User should be able to write a tip on topic(business/restaurant).



**Testing**

Testing can be done by starting the server, and copy and paste the following urls to the browser.

By checking the return objects values, once could determine the result of the execution.



**Register**

```

```



**Login**

```

```



**Refresh new reviews**

```

```



**Make friend request**

```

```



**Accept/Reject friend request**

```

```



**Vote(useful, funny, cool) review**

```

```



**Follow User**

```

```



**Choose Elite User**

```

```



**Reply Review**

```

```



**Upvote a Tip**

```

```



**Create a Group**

```

```



**Join an existing group**

```

```



**Follow a Business(Restaurant)**

```

```



**Write a Review on a Business(Restaurant)**

```

```



**Write a Tip on a Business(Restaurant)**

```

```

