import mysql.connector
import json
import ast

def connectDB():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="15625067696aA",
        database="yelp",
        auth_plugin='mysql_native_password'
    )

    return mydb


def generateFriends(path):
    file_name = "generateFriends"
    file_count = 1
    gff =  open("generateFriends"+str(file_count)+".sql", "a")
    gff.write("BEGIN;\n")

    with open(path) as f:
        count = 0
        batch_size = 100000
        for line in f:

            data = json.loads(line)
            friends = data["friends"]
            user_id = data["user_id"]
            batch_size-=1
            if friends is not None:
                friends_list = friends.split(',')
                friends_list = [friend.strip() for friend in friends_list]
                print(" %d / 1637138"%(count), end='\r')

                tmp = ""
                tmp += "\ninsert into friend values "
                for friend in friends_list:
                    tmp += "(\'"+user_id+"\', \'"+friend+"\'),"
                tmp = tmp[:-1]
                tmp+=";"
            gff.write(tmp)
            if batch_size == 0:
                gff.write("\nCOMMIT;")
                gff.close()
                file_count+=1
                gff =  open("generateFriends"+str(file_count)+".sql", "a")
                batch_size = 100000
            count += 1
        gff.write("\nCOMMIT;")
        gff.close()


if __name__ == "__main__":
    user_file_path = "../yelp_dataset/user.json"
    photo_file_path = "yelp_dataset/photo.json"
    tip_file_path = "yelp_dataset/tip.json"
    review_file_path = "yelp_dataset/review.json"
    checkin_file_path = "yelp_dataset/checkin.json"
    business_file_path = "../yelp_dataset/business.json"
    attributes_out_path = "./attributes.json"
    category_out_path = "./categories.json"
    # populateUser(user_file_path)
    # checkAttributes(business_file_path, out_path)
    # checkCategories(business_file_path, category_out_path)
    # createAttributesTables(category_out_path)
    # populateAttributes(business_file_path)
    # populateUser(user_file_path)
    # db = connectDB()
    # checkBusiness(business_file_path, db)
    generateFriends(user_file_path)
    print("finish")
