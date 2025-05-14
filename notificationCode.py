import smtplib
import ssl
from email.message import EmailMessage

def sendEmail(email_reciever, subject, body):
    email_sender = 'kdoggylol10@gmail.com'
    email_password = 'yglu htyh ndhx pqyq'
    #email_reciever = '27047602@students.lincoln.ac.uk'

    #subject = 'Someone has posed a threat to our System!!'
    #body = """
    #Someone has tried to enter our system without authorisation! Please act quickly to stop this.
    #"""
    em = EmailMessage()

    em['From'] = email_sender
    em['To'] = email_reciever
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context= context) as smtp:
        smtp.login(email_sender , email_password)
        smtp.sendmail(email_sender, email_reciever, em.as_string())


class AdminEmails:
    def __init__(self):
        # 1. Settup variables
        self.emails = list()
        self.filename = "AdminEmailAddresses.txt"
        # 2. Open "AdminEmailAddresses.txt"
        file_content = None
        try:
            file = open(self.filename, 'r')
            file_content = file.read()
            file.close()
            print("Database Openned")
        except FileNotFoundError:
            print(f"ERROR: file \"{self.filename}\" could not be found")
            print("Open Database Failed.")
            return
        # 3. converts the raw data into a format suitable to store
        file_content = file_content.split('\n')
        for email in file_content:
            self.emails.append(email)
    def Save(self):
        output = ""
        # 1. Convert "self.emails" into a continuous string (called "output") to store in a file
        if len(self.emails) > 0:
            output = self.emails[0]
            del self.emails[0]
            for email in self.emails:
                output += '\n'
                output += email
        # 2. Save "output" in "AdminEmailAddresses.txt"
        try:
            file = open(self.filename, 'w')
            file.write(output)
            file.close()
            print("List of Admin Emails saved")
        except FileNotFoundError:
            print(f"ERROR: AdminEmails: Save(): file \"{self.filename}\" could not be found")
            print("List of Admin Emails could not be saved")
    def Add(self, email):
        self.emails.append(email)
        self.Save()
    def Remove(self, index):
        del self.index[index]
        self.Save()
    
admin_emails = AdminEmails()