from django.contrib.auth.models import User

def validateSong(data, action = None):
    """
    Validate song data.
    """
    message = []
    
    if data["title"] is None:
        message.append("title is required")
    if data["artist"] is None:
        message.append("artist is required")


    # if not User.objects.filter(pk=data["user"]).exists():
    #     message.append("User field does not exist")

    if data["file_url"] is None:
        message.append("file_url is required")
    else:
        #file_type = data["file_url"].content_type.split('/')[1]
        #print(data["file_url"].content_type)
        file_size = data["file_url"].size
        # if file_type != "mp3":
        #     message.append("File type must be 'mp3'" )
        if file_size > (25*1024*1024):
            # less than 25mb
            message.append("File size must be less than 25 MB")

    if len(message) > 0:
        return [False, ", ".join(message)]

    return [True, ""]

def validateAlbum(data, action = None):
    """
    Validate album data.
    """
    message = []
    if data["title"] is None:
        message.append("Title must not be empty")

    image_types = ("png", "jpg", "jpeg", "gif", "bmp","jfif")
    if data["image_album"] is None:
        message.append("image_album is required")
    else:
        file_type = data["image_album"].content_type.split('/')[1]
        file_size = data["image_album"].size
        if file_type not in image_types:
            message.append(f"File type must be in {image_types.__str__()}" )
        if file_size > (25*1024*1024):
            # less than 25mb
            message.append("File size must be less than 25 MB")
    
    if len(message) > 0:
        return (False, ", ".join(message))
    return (True, "")
    