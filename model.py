
def create_collections(db):
    global current_collection
    current_collection = db.CurrentUser
    global image_collection
    image_collection = db.Images
    global user_image_collection
    user_image_collection = db.UserImages
    global user_collection
    user_collection = db.Users

def check_for_user(db):
    result = current_collection.find_one({})
    return result != None

def get_current_user_info(db):
    result = current_collection.find_one({})
    if not result:
        raise Exception("No user logged in.")
    return dict(result)

def attempt_sign_in(db, username, password):
    user_info = {"username": username, "password": password}
    # If username and password is not found, register a new user.
    result = user_collection.find_one(user_info)
    if not result:
        user_collection.insert_one(user_info)
        result = user_collection.find_one(user_info)
    users = dict(result)
    current_collection.insert_one({"user_id": users["_id"], "username": username})

def upload_photo(db, img_link):
    image_info = {"img_link": img_link}
    result = image_collection.find_one(image_info)
    if not result:
        # If image does not exist in database, upload to images database.
        image_collection.insert_one(image_info)
    # Upload to images connected to user_id.
    user_info = get_current_user_info(db)
    user_id = user_info["user_id"]
    result = user_image_collection.find_one({"user_id": user_id})
    if not result:
        user_image_collection.insert_one({"user_id": user_id, "images": [img_link]})
    else:
        user_images_list = dict(result)["images"]
        if img_link not in user_images_list:
            user_images_list.append(img_link)
            result = user_image_collection.replace_one({"user_id": user_id}, {"user_id": user_id, "images": user_images_list})

def list_images(db, user_id):
    result = user_image_collection.find_one({"user_id": user_id})
    if not result:
        return []
    user_images_list = dict(result)["images"]
    return user_images_list

def list_all_images(db):
    all_img_list = []
    # This is a random sampling (sort) with a limit of 50 results to avoid overloading page.
    results = image_collection.aggregate([{"$sample": { "size": 50 }}])
    for result in results:
        image_doc = dict(result)
        all_img_list.append(image_doc["img_link"])
    return all_img_list

def attempt_sign_out(db):
    current_collection.find_one_and_delete({})





    
