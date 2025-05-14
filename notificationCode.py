import smtplib
import ssl
from email.message import EmailMessage

email_sender = 'kdoggylol10@gmail.com'
email_password = 'yglu htyh ndhx pqyq'
email_reciever = '27047602@students.lincoln.ac.uk'


subject = 'Someone has posed a threat to our System!!'

body = """
Someone has tried to enter our system without authorisation! Please act quickly to stop this.
"""


em = EmailMessage()

em['From'] = email_sender
em['To'] = email_reciever
em['subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context= context) as smtp:
    smtp.login(email_sender , email_password)
    smtp.sendmail(email_sender, email_reciever, em.as_string())