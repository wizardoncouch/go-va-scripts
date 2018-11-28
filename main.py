from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

__author__ = 'axclgo'

import mysql.connector
import boto3
from dotenv import load_dotenv
import os
import smtplib

load_dotenv(verbose=True)


class SendMail:
    aws_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    s3 = None
    myDb = None

    def Process(self):
        self.s3Connect()
        self.send()
        print(self.s3)

    def Resumes(self):
        pass

    def send(self, name, file):
        from_address = os.getenv('MAIL_FROM')
        to_address = os.getenv('MAIL_RECIPIENTS')
        mail_password = os.getenv('MAIL_PASSWORD')

        msg = MIMEMultipart()

        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = 'New applicant resume.'

        body = 'Here are the list of resumes\' of the new applicants'

        msg.attach(MIMEText(body, 'plain'))

        extension = file.split('.')[-1]
        filename = '{name}.{extension}'.format(name=name, extension=extension)
        attachment = open(file, "rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_address, mail_password)
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()

    def s3Connect(self):
        try:
            self.s3 = boto3.client(
                's3',
                aws_access_key_id='',
                aws_secret_access_key=''
            )
        except:
            print('Something went wrong')

    def mysqlConnect(self):
        self.myDb = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd=''
        )


mailer = SendMail()
mailer.Process()
