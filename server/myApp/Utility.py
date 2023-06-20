from django.conf import settings
from django.core.mail import send_mail
link = "http://localhost:8000/"
def sendmail_wo_cc(subject: str, body: str, to: list):
    email_from = settings.EMAIL_HOST_USER
    pwd = settings.EMAIL_HOST_PASSWORD
    err = []
    if not subject:
        err.append("Subject cannot be null")
    if not body:
        err.append("Body cannot be null")
    if (not to or len(to) == 0):
        err.append("To cannot be null")

    if len(err) > 0:
        return [False, ", ".join(err)]
    send_mail( subject,message=body, from_email=email_from, recipient_list=to,html_message= body)
    return [True, "Send mail successfully"]


def sendmail_forgot_pwd(to:str):
    emailto = [to]
    subject = "[announded]Reset password"
    url = "<a href='"+link+"/test/forgetpwd' />Click here to change your password</a>"
    body = "Hi there,<br/>"
    body += "There was a request to change your password!<br/>"
    body += "Otherwise, please click this link to change your password:<br/>"
    body += url+"<br/>"
    body += "<br/> Regards"
    body += "Owner"
    sendmail_wo_cc(subject=subject, body=body, to=emailto)

