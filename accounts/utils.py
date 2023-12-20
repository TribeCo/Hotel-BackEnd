from config.settings import hotel_email,password_email
from email.message import EmailMessage
import smtplib
#-----------------------------------------------------------
def send_code_mail(send_to,code):

    msg = EmailMessage()
    msg['Subject'] = 'کد اعتبار سنجی سایت هتل'
    msg['From'] = hotel_email
    msg['To'] = send_to
    msg.set_content(f"کد شما: {code}")

    with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
        server.login(hotel_email,password_email)
        server.send_message(msg)
#-----------------------------------------------------------
def send_mail(name,subject,text,email):

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = hotel_email
    msg['To'] = "TahaM8000@gmail.com"
    msg.set_content(f"{name} در نظرات نوشت :   {text} \n ایمیل کاربر : {email}")

    with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
        server.login(hotel_email,password_email)
        server.send_message(msg)
#-----------------------------------------------------------
