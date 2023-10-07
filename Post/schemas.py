def postEntity(item)-> dict:
    return {
        "id": str(item["_id"]),
        "username": item["username"],
        "image_url": item["image_url"],
        "texts":item["texts"]
    }

def postsEntity(entity)->list:
    return [postEntity(item) for item in entity]