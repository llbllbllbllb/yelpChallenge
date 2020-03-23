import mysql.connector
import json
import ast
import os


def connectDB():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="15625067696aA",
        database="yelp",
        auth_plugin='mysql_native_password'
    )

    return mydb


def checkAttributes(path, out):
    res = {}
    type_s = set()
    with open(path) as f:
        for line in f:
            # print(line)
            data = json.loads(line)
            if data["attributes"] != None:
                for k, v in data['attributes'].items():
                    # string to dict
                    temp = ast.literal_eval(v)
                    if k not in res:
                        res[k] = dict()
                    # if data["business_id"] not in res:
                    #     res[data["business_id"]] = dict()
                    #     res[data["business_id"]]["attributes"] = dict()
                    # print(type(v))
                    # if v[0] == "{":
                    #     res[data['business_id']]["attributes"][k] = v
                    # print(v)
                        # temp = v.encode('utf-8')
                        # temp = str(v);
                        # temp = json.loads(temp)
                        # type_s.add(type(v))
                        try:
                            for kk, vv in temp.items():
                                if kk not in res[k]:
                                    res[k][kk] = dict()
                                res[k][kk] = vv
                        except:
                            continue
                    else:
                        try:
                            for kk, vv in temp.items():
                                if kk not in res[k]:
                                    print("error", kk)
                        except:
                            continue

    print(type_s)
    # element = None
    # key = None
    # print(len(res.keys()))
    # for k, v in res.items():
    #     for kk, vv in v.items():
    #         # print(len(vv))
    #         if element is None or len(vv) > len(element):
    #             element = vv
    #             key = k
    # print(element)
    with open(out, 'w') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)
    return res

def populateAttributes(path):
    mydb = connectDB()
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM attributes;")
    cursor.execute("DELETE FROM attrAmbience;")
    cursor.execute("DELETE FROM attrBestNights;")
    cursor.execute("DELETE FROM attrBusinessParking;")
    cursor.execute("DELETE FROM attrDietaryRestrictions;")
    cursor.execute("DELETE FROM attrGoodForMeal;")
    cursor.execute("DELETE FROM attrHairSpecializesIn;")
    cursor.execute("DELETE FROM attrMusic;")
    mydb.commit()
    total = 0
    with open(path) as f:
        for line in f:
            total += 1
    print("total", total)
    count = 0
    with open(path) as f:
        for line in f:
            # print(line)
            data = json.loads(line)
            id = data["business_id"].strip()
            print(" %d / %d"%(count, total), end='\r')
            if data["attributes"] != None:
                singleAttributes = {}
                # print("-----1----")
                for k, v in data['attributes'].items():
                    temp = ast.literal_eval(v)
                    k_name = k.strip()
                    str_multiple_attributes = "INSERT INTO attr" + k_name + " (business_id"
                    if isinstance(temp, dict):
                        for kk in temp.keys():
                            kk = kk.replace('-', '_')
                            str_multiple_attributes += ", " + kk
                        str_multiple_attributes += ") VALUES ('" + id + "'"
                        for vv in temp.values():
                            str_multiple_attributes += ", " + str(vv)
                        str_multiple_attributes += ");"
                        print(str_multiple_attributes)
                        try:
                            cursor.execute(str_multiple_attributes)
                            mydb.commit()
                        except mysql.connector.Error as error:
                            print(error)
                            mydb.rollback()
                            cursor.close()
                            mydb.close()
                            return
                    else:
                        v_value = str(v.strip())
                        if v_value is not None and v_value.upper() != 'NONE':
                            singleAttributes[k_name] = v_value
                str_single_attributes = "INSERT INTO attributes (business_id"
                for k in singleAttributes.keys():
                    k = k.replace('-', '_')
                    str_single_attributes = str_single_attributes +", " + k
                str_single_attributes += ") VALUES ('" + id + "'"
                for v in singleAttributes.values():
                    if v[0] == 'u' or v[0] == 'b':
                        v = v[1:]
                    str_single_attributes += ", " + str(v)
                str_single_attributes += ");"
                # print(str_single_attributes)
                try:
                    cursor.execute(str_single_attributes)
                    mydb.commit()
                except mysql.connector.Error as error:
                    print(error)
                    mydb.rollback()
                    cursor.close()
                    mydb.close()
                    return
            count += 1
                # print("-----2----")


                    # type_set.add(type(temp))

    # element = None
    # key = None
    # print(len(res.keys()))
    # for k, v in res.items():
    #     for kk, vv in v.items():
    #         # print(len(vv))
    #         if element is None or len(vv) > len(element):
    #             element = vv
    #             key = k
    # print(element)
    # return res


def checkCategories(path, out):
    res = {}
    category_set = set()
    with open(path) as f:
        for line in f:
            data = json.loads(line)
            if data["business_id"] not in res:
                # temp = ast.literal_eval(data["categories"])
                res[data["business_id"]] = data["categories"]

                if data["categories"] is not None:
                    for i in data["categories"].split(','):
                        category_set.add(i)
            else:
                print("duplicate id found")
    # with open(out, 'w') as f:
    #     json.dump(res, f, ensure_ascii=False, indent=4)
    print(category_set)
    print(len(category_set))

def populateUser(path):
    mydb = connectDB()
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM user")
    mydb.commit()
    with open(path) as f:
        count = 0
        for line in f:
            data = json.loads(line)
            friends = data["friends"]
            user_id = data["user_id"]
            name = data["name"]
            review_count = data["review_count"]
            yelping_since = data["yelping_since"]
            useful = data["useful"]
            funny = data["funny"]
            cool = data["cool"]
            fans = data["fans"]
            average_stars = data["average_stars"]
            compliment_hot = data["compliment_hot"]
            compliment_more = data["compliment_more"]
            compliment_profile = data["compliment_profile"]
            compliment_cute = data["compliment_cute"]
            compliment_list = data["compliment_list"]
            compliment_note = data["compliment_note"]
            compliment_plain = data["compliment_plain"]
            compliment_cool = data["compliment_cool"]
            compliment_funny = data["compliment_funny"]
            compliment_writer = data["compliment_writer"]
            compliment_photos = data["compliment_photos"]
            insert_query = "INSERT INTO user (user_id, name, review_count, yelping_since, useful, funny, cool, fans, average_stars, compliment_hot, compliment_more, compliment_profile, compliment_cute, compliment_list, compliment_note, compliment_plain, compliment_cool, compliment_funny, compliment_writer, compliment_photos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            val = (user_id, name, review_count, yelping_since, useful, funny, cool, fans, average_stars, compliment_hot, compliment_more, compliment_profile, compliment_cute, compliment_list, compliment_note, compliment_plain, compliment_cool, compliment_funny, compliment_writer, compliment_photos)

            try:
                cursor.execute(insert_query, val)
                mydb.commit()
                print(" %d / 1637138"%(count), end='\r')
            except mysql.connector.Error as error:
                print(error)
                mydb.rollback()
                cursor.close()
                mydb.close()
                return
            count += 1

    cursor.close()
    mydb.close()
    print(count)

def populateFriends(path):
    mydb = connectDB()
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM friend;")
    mydb.commit()
    with open(path) as f:
        count = 0
        for line in f:
            data = json.loads(line)
            friends = data["friends"]
            user_id = data["user_id"]
            if friends is not None:
                friends_list = friends.split(',')
                friends_list = [friend.strip() for friend in friends_list]
                print(" %d / 1637138"%(count), end='\r')
                for friend in friends_list:
                    # friend user_id may not in the user table
                    # select_query  = "SELECT user_id FROM user WHERE user_id = '" + friend + "';"
                    # cursor.execute(select_query)
                    # result_exist = cursor.fetchall()
                    #
                    # if result_exist is None or len(result_exist) == 0:
                    #     continue
                    query = "INSERT INTO friend (user_id, friend_id) VALUES (%s, %s);"
                    value = (user_id, friend)

                    try:
                        # print(value)
                        cursor.execute(query, value)
                        mydb.commit()

# https://yelp-dataset.s3.amazonaws.com/YDC14/yelp_dataset.tgz?Signature=4kJOz99XxDBiIusBUHovwN19i1M%3D&Expires=1584818217&AWSAccessKeyId=AKIAJ3CYHOIAD6T2PGKA
                    except mysql.connector.Error as error:
                        # print(error)
                        continue
                        # mydb.rollback()
                        # cursor.close()
                        # mydb.close()
                        # return
            count += 1
        cursor.close()
        mydb.close()


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
            # ('rvtLwn1raY-MjrTATz8Ogg','zJFCS9vn2PuQqRsWg6Gb1w','16Fplxu-OwVmTEFxQAUP4g','1.0','2018-07-14','16:01:46',"Worst service ever. Manager didnt care. Photographer was rude. Asked to be called back and never happened",'0','0','0'),('0t62T22zCEiv-rjRGPL-Aw','FGMtqYSHcjAnH5YVoDKCvQ','GMrwDXRlAZU2zj5nH6l4vQ','2.0','2017-10-19','07:32:31',"ORDERED TO GO today  ... always get our breakfast sandwich order here when I'm in Vegas. Today sandwiches were AWFUL. The bread today are BRICK HARD. SUCKS  I understand when trying to save money. BUT THIS SUCKS .. maybe we should stick with PHO from now on  \¿¿¿¿\",'0','0','0')

            value = "(\'"+str(review_id)+"\',"+"\'"+ str(user_id)+"\',"+"\'"+ str(business_id)+"\',"+"\'"+ str(stars)+"\',"+"\'"+ str(reviewDate)+"\',"+"\'"+str(reviewTime)+"\',"+"\""+ str(reviewText)+"\","+"\'"+ str(useful)+"\',"+"\'"+ str(funny)+"\',"+"\'"+ str(cool)+"\')"

            batch_size-=1;
            if batch_size == 0:
                value += ";"
                batch_size = set_batch_size
            else:
                value += ","

            gff.write(value)
            # test_size-=1
            # if test_size == 0:
            #     gff.write(";\n")
            #     gff.write("\nCOMMIT;")
            #     gff.close()
            #     exit()


    gff.write(";")
    gff.write("\nCOMMIT;")
    gff.close()


def populateTip(tip_file_path):
    mydb = connectDB()
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM tip;")

    with open(review_file_path) as f:
        count = 0
        for line in f:
            print(" %d / total_size"%(count), end='\r')
            data = json.loads(line)

            business_id = data["business_id"]
            user_id = data["user_id"]
            tipText = data["text"]
            postDate = data["date"]
            compliment_count = ["compliment_count"]

            # process postDate






def checkBusiness(business_file_path, db):
    mycursor = db.cursor()
    mycursor.execute("delete from business;")
    db.commit()
    total_line = 0
    with open(business_file_path) as f:

            for line in f:
                total_line += 1
            print("total_line:", total_line)
    with open(business_file_path) as f:


        i = 0
        colDict = ['business_id','name','address','city','state','postal_code','latitude','longitude','stars','review_count','is_open']
        for line in f:
            print('Progress: %d / %d'%(i,total_line) , end='\r')
            data = json.loads(line)
            sql = "insert into business (business_id,name,address,city,state,postal_code,latitude,longitude,stars,review_count,is_open) values ("

            for key in colDict:

                sql += '"'+str(data[key]).replace('"',"'")+'",'
            sql = sql[:-1]
            sql += ");"
            # print(sql)
            mycursor.execute(sql)
            db.commit()

            i+=1

if __name__ == "__main__":
    user_file_path = "../yelp_dataset/user.json"
    photo_file_path = "yelp_dataset/photo.json"
    tip_file_path = "../yelp_dataset/tip.json"
    review_file_path = "../yelp_dataset/review.json"
    checkin_file_path = "yelp_dataset/checkin.json"
    business_file_path = "../yelp_dataset/business.json"
    attributes_out_path = "./attributes.json"
    category_out_path = "./categories.json"
    # populateUser(user_file_path)
    # checkAttributes(business_file_path, out_path)
    # checkCategories(business_file_path, category_out_path)
    # createAttributesTables(category_out_path)
    # # populateAttributes(business_file_
    populateTip(tip_file_path)
    # populateUser(user_file_path)
    # db = connectDB()
    # checkBusiness(business_file_path, db)
    # populateReview(user_file_path)
    print("finish")
