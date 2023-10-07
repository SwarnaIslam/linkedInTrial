def notificationEntity(item)-> dict:
    return {
        "postId": str(item["postId"]),
        "username": item["username"],
        "timestamp": item["timestamp"],
        "message":item["message"]
    }

def notificationsEntity(entity)->list:
    return [notificationEntity(item) for item in entity]