**ECE656 Project Report: A Simple Social Network (with Yelp Dataset)**

Libang Liang

Zhiming Lin



#### 1. ER Model

#### 2. Create Tables

#### 3. Populating the data

Total size of the JSON data: 9.8GB

We first used Python Script to generate SQL batched insert statement to insert large JSON file.

**Implementation** 

Take review as an example:

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





#### 4. Client

We created set of APIs using Java with Spring Boot Framwork. User can do the following functions:

1. Register

2. Login

3. Refresh new reviews if they followed any business(restaurant) or friends

4. Make friend request

5. Accept/Reject friend request

6. Vote(useful, funny, cool) review

7. Follow User

8. Choose Elite User

9. Reply Review

10. Upvote a Tip

11. Create a Group

12. Join an existing group

13. Follow a Business(Restaurant)

14. Write a Review on a Business(Restaurant)

15. Write a Tip on a Business(Restaurant)

    