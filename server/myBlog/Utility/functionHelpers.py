from django.contrib.auth.models import User
def validatePost(data, action=None):
    message = []
    if action != "update":
        if data["user"] is None:
            message.append("User field cannot be blank")
        elif not data["user"].isdigit():
            message.append("User field cannot be a string")
        elif not User.objects.filter(pk=data["user"]).exists():
            message.append("User field does not exist")

    if data["content"] is None:
        message.append("Content field cannot be blank")
    image_types = ("png", "jpg", "jpeg", "gif", "bmp","jfif")
    if data["file"] is not None:
        file_type = data["file"].content_type.split('/')[1]
        file_size = data["file"].size
        if file_type not in image_types:
            message.append("File type must be %s" % image_types.__str__())
        if file_size > (25*1024*1024):
            # less than 25mb
            message.append("File size must be less than 25 MB")
        
    if len(message) > 0:
        return [False, ",".join(message)]
    
    return [True,""]