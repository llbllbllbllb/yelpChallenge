import mysql.connector
import json
import ast

def ConnectDB():
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




if __name__ == "__main__":
    user_file_path = "/yelp_dataset/user.json"
    photo_file_path = "/yelp_dataset/photo.json"
    tip_file_path = "/yelp_dataset/tip.json"
    review_file_path = "/yelp_dataset/review.json"
    checkin_file_path = "/yelp_dataset/checkin.json"
    business_file_path = "yelp_dataset/business.json"
    out_path = "./attributes.json"
    category_out_path = "./categories.json"
    # PopulateUser(user_file_path)
    # checkAttributes(business_file_path, out_path)
    checkCategories(business_file_path, category_out_path)
    print("finish")