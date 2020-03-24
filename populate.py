import mysql.connector
import json
import ast
import os


import time


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
                        # print(str_multiple_attributes)

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

def populateElite(path):
    mydb = connectDB()
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM eliteYear;")
    mydb.commit()
    out_file_path = "./eliteYear_data.sql"
    count = 0
    total = 1000
    with open(out_file_path, 'w') as fd:
        fd.write('BEGIN;\n')
        fd.close()

    print("total: ", total)
    insert_query = "INSERT INTO eliteYear VALUES ";
    with open(path) as f:
        for line in f:
            data = json.loads(line)
            user_id = data["user_id"].strip()
            elites = data["elite"]

            print("progress: %d / %d "%(count, total), end='\r')

            elites_list = elites.split(',')

            if elites != None and len(elites) != 0:
                for elite_index in range(len(elites_list)):
                    year = elites_list[elite_index].strip()
                    if count == 0:
                        insert_query += "('%s', %s)"%(user_id, year)
                    else:
                        insert_query += ", ('%s', %s)"%(user_id, year)
                    count += 1
            if count > total:
                with open(out_file_path, 'a') as fd:
                    insert_query += ";"
                    fd.write(insert_query)
                    fd.write('\n')
                    count = 0
                    insert_query = "INSERT INTO eliteYear VALUES ";
                    fd.close()
                    # try:
                    #     cursor.execute(insert_query, val)
                    #     mydb.commit()
                    # except mysql.connector.Error as error:
                    #     print(error)
                    #     print(val)
                    #     print(insert_query)
                    #     mydb.rollback()
                    #     cursor.close()
                    #     mydb.close()
                    #     return

    with open(out_file_path, 'a') as fd:
        if len(insert_query) > 30:
            insert_query += ";"
            fd.write(insert_query)
            fd.write('\n')
        fd.write('COMMIT;\n')
        fd.close()
def populateUser(path):
    mydb = connectDB()
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM user;")
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
    if os.path.exists("generateTip.sql"):
        os.remove("generateTip.sql")

    gff =  open("generateTip.sql", "a")
    gff.write("DELETE FROM tip;\n")
    gff.write("BEGIN;\n")

    count = 0
    set_batch_size = 100
    batch_size = set_batch_size

    with open(tip_file_path) as f:
        count = 0

        query = "\n INSERT INTO tip (business_id,user_id, tipText,postDate,postTime,compliment_count) VALUES "
        for line in f:
            print(" %d / 1223094"%(count), end='\r')
            if batch_size == set_batch_size:
                gff.write(query)
            data = json.loads(line)


            business_id = data["business_id"]
            user_id = data["user_id"]
            tipText = data["text"]
            date_time = data["date"]
            compliment_count = data["compliment_count"]

            postDate,postTime = date_time.split()

            tipText = tipText.replace('"',"")
            tipText = tipText.replace(';',"")
            tipText = tipText.replace('\\', '/ ')

            value = "(\'" + str(business_id) + "\',\'" + str(user_id) + "\',\"" + str(tipText) + "\",\'" + str(postDate) + "\',\'" + str(postTime) + "\',\'" + str(compliment_count) + "\')"

            batch_size-=1;
            if batch_size == 0 or count == 1223093:
                value += ";"
                batch_size = set_batch_size
            else:
                value += ","

            gff.write(value)
            count += 1


    gff.write(";")
    gff.write("\nCOMMIT;")
    gff.close()





            # process postDate

def populateCategories(path):
    mydb = connectDB()
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM CATEGORIES;")
    mydb.commit()

    count = 0
    with open(path) as f:
        for line in f:
            data = json.loads(line)
            id = data['business_id'].strip()
            categories = data['categories']

            print(" %d / 192609"%(count), end='\r')
            count += 1

            if categories is not None and len(categories) != 0:
                categories_list = categories.split(',')
                for category in categories_list:
                    category = category.strip()
                    insert_query = "INSERT INTO categories (business_id, category) VALUES ('" + id + "'" + ", \"" + category + "\");"
                    # print(insert_query)
                    try:
                        cursor.execute(insert_query)
                        mydb.commit()
                    except mysql.connector.Error as error:
                        continue

def populateHours(path):
    mydb = connectDB()
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM hours;")
    mydb.commit()
    count = 0
    total = 0
    with open (path) as f:
        for line in f:
            total += 1

    with open(path) as f:
        for line in f:
            data = json.loads(line)
            hours = data['hours']
            id = data['business_id'].strip()

            print(" %d / %d"%(count, total), end='\r')
            count += 1

            if hours is not None and len(hours) != 0:
                insert_query = "INSERT INTO hours (business_id"
                for k in hours.keys():
                    ele = k.strip().upper()
                    if ele == "MONDAY":
                        insert_query = insert_query +  ", mondayStart, " + "mondayEnd"
                    elif ele == "TUESDAY":
                        insert_query = insert_query + ", tuesdayStart, " + "tuesdayEnd"
                    elif ele == "WEDNESDAY":
                        insert_query = insert_query + ", wednesdayStart, " + "wednesdayEnd"
                    elif ele == "THURSDAY":
                        insert_query = insert_query + ", thursdayStart, " + "thursdayEnd"
                    elif ele == "FRIDAY":
                        insert_query = insert_query + ", fridayStart, " + "fridayEnd"
                    elif ele == "SATURDAY":
                        insert_query = insert_query + ", saturdayStart, " + "saturdayEnd"
                    elif ele == "SUNDAY":
                        insert_query = insert_query + ", sundayStart, " + "sundayEnd"
                insert_query += ") VALUES ('" + id + "'"
                for v in hours.values():
                    periods = v.split('-')
                    for index in range(len(periods)):
                        time_string = time.strptime(periods[index], "%H:%M")
                        periods[index] = time.strftime("%H:%M:%S", time_string)
                    # for index in range(len(periods)):
                    #     period_list = periods[index].split(":")
                    #     for l in range(len(period_list)):
                    #         if len(period_list[l]) < 2:
                    #             period_list[l] = "0" + period_list[l]
                    #     if len(period_list) < 3:
                    #         period_list.append("00")
                    #     periods[index] = ":".join(period_list)
                    insert_query = insert_query + ", '" + periods[0] + "', '" + periods[1] + "'"
                insert_query += ");"
                # print(insert_query)
                try:
                    cursor.execute(insert_query)
                    mydb.commit()
                except mysql.connector.Error as error:
                    print(error)
                    mydb.rollback()
                    cursor.close()
                    mydb.close()
                    return

def populatePhotos(path):
    db = connectDB()
    cursor = db.cursor()
    cursor.execute("DELETE FROM photo;")
    db.commit()
    out_path = './photo_data.sql'
    with open(out_path, 'w') as f:
        f.write("BEGIN;\n")
        f.close()
    total = 50
    count  = 0
    insert_query = "INSERT INTO photo VALUES "
    with open(path) as f:
        for line in f:
            print("%d / %d"%(count, total), end='\r')
            data = json.loads(line)
            photo_id = data["photo_id"]
            business_id = data["business_id"]
            caption = data["caption"]
            if caption is None:
                caption = ""
            else:
                caption = caption.replace("\"", "'").replace('"',"'").strip("'")
            label = data["label"]
            if label is None:
                label = ""
            else:
                label = label.replace("\"", "'").replace('"',"'").strip("'")

            if count == 0:
                insert_query += "(\"%s\", \"%s\", \"%s\", \"%s\")"%(photo_id, business_id, caption, label)
            else:
                insert_query += ", (\"%s\", \"%s\", \"%s\", \"%s\")"%(photo_id, business_id, caption, label)
            count += 1
            if count > total:
                with open(out_path, 'a') as fd:
                    insert_query += ";"
                    fd.write(insert_query)
                    fd.write('\n')
                    count = 0
                    insert_query = "INSERT INTO photo VALUES ";
                    fd.close()


    with open(out_path, 'a') as fd:
        if len(insert_query) > 25:
            insert_query += ";"
            fd.write(insert_query)
            fd.write('\n')
        fd.write('COMMIT;\n')
        fd.close()




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

def populateCheckin(path):
    if os.path.exists("generateCheckin.sql"):
        os.remove("generateCheckin.sql")

    gff =  open("generateCheckin.sql", "a")
    gff.write("DELETE FROM checkin;\n")
    gff.write("BEGIN;\n")
    total = 0
    count = 0
    set_batch_size = 500
    batch_size = set_batch_size
    with open(path) as f:
        query = "\n INSERT INTO checkin (business_id,checkinDate,checkinTime) VALUES "
        for line in f:

            print("%d / %d"%(count, 161950), end='\r')
            data = json.loads(line)
            business_id = data["business_id"]
            date = data["date"]

            date_time_list = date.split(', ')

            for date_time in date_time_list:
                if batch_size == set_batch_size:
                    gff.write(query)
                date,time = date_time.split()
                value = "('" + str(business_id) + "','" + str(date) + "','" + str(time) + "')"
                batch_size-=1;
                if batch_size == 0 or date_time == date_time_list[-1]:
                    value += ";"
                    batch_size = set_batch_size
                else:
                    value += ","

                gff.write(value)
            count += 1

    gff.write(";")
    gff.write("\nCOMMIT;")
    gff.close()



if __name__ == "__main__":
    user_file_path = "../yelp_dataset/user.json"

    photo_file_path = "yelp_dataset/photo.json"
    tip_file_path = "../yelp_dataset/tip.json"
    review_file_path = "../yelp_dataset/review.json"

    checkin_file_path = "../yelp_dataset/checkin.json"
    business_file_path = "../yelp_dataset/business.json"
    attributes_out_path = "./attributes.json"
    category_out_path = "../yelp_dataset/categories.json"


    populateCheckin(checkin_file_path)

    print("finish")
