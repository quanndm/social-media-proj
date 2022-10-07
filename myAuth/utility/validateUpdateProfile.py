from datetime import datetime
from django.contrib.auth.models import User
def validateUpdateProfile(new_data, user_id):
    # initializing format
    format = "%d-%m-%Y"
    res = True
    arrErr = []
    #----start validate---------------
    if User.objects.exclude(pk=user_id).filter(username=new_data["user_name"]).exists():
        arrErr.append("This username is already in use") 

    if User.objects.exclude(pk=user_id).filter(email=new_data["email"]).exists():
        arrErr.append("This email is already in use")

    if new_data["gender"] not in ("M", "F"):
        arrErr.append("Gender Must be M or F")
    # validate birth date
    if not new_data["DOB"]:
        arrErr.append("DOB cannot be blank")

    try:
        res = bool(datetime.strptime(new_data["DOB"], format))
    except ValueError:
        res = False
    if res == False:
        arrErr.append("Birthdate must be formatted correctly: dd-mm-yyyy")

    if len(arrErr) > 0:
        return [False, ','.join(arrErr)]
    return [True, ""]