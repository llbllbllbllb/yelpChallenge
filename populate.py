import mysql.connector
import json
import ast

def connectDB():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="mysql",
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
                    select_query  = "SELECT user_id FROM user WHERE user_id = '" + friend + "';"
                    cursor.execute(select_query)
                    result_exist = cursor.fetchall()

                    if result_exist is None or len(result_exist) == 0:
                        continue
                    query = "INSERT INTO friend (user_id, friend_id) VALUES (%s, %s);"
                    value = (user_id, friend)

                    try:
                        # print(value)
                        cursor.execute(query, value)
                        mydb.commit()


                    except mysql.connector.Error as error:
                        print(error)
                        mydb.rollback()
                        cursor.close()
                        mydb.close()
                        return
            count += 1
        cursor.close()
        mydb.close()

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
    tip_file_path = "yelp_dataset/tip.json"
    review_file_path = "yelp_dataset/review.json"
    checkin_file_path = "yelp_dataset/checkin.json"
    business_file_path = "../yelp_dataset/business.json"
    attributes_out_path = "./attributes.json"
    category_out_path = "./categories.json"
    # PopulateUser(user_file_path)
    # checkAttributes(business_file_path, out_path)
    # checkCategories(business_file_path, category_out_path)
    # createAttributesTables(category_out_path)
    populateAttributes(business_file_path)
    # populateUser(user_file_path)
    # db = connectDB()
    # checkBusiness(business_file_path, db)
    # populateFriends(user_file_path)
    print("finish")
