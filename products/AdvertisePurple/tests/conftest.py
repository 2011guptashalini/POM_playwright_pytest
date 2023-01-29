import logging
import os

import pymysql
import pytest
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

import sshtunnel

from products.AdvertisePurple.utils import ap_mysql_delete as AP_MYSQL

from dotenv import load_dotenv

load_dotenv()


URL_INTERNAL = os.getenv("URL_INTERNAL")
URL_API = os.getenv("URL_API")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
LOGIN = '/login'

SSH_ADDRESS_OR_HOST = os.getenv("SSH_ADDRESS_OR_HOST")
SSH_PORT = int(os.getenv("SSH_PORT"))
SSH_USERNAME = os.getenv("SSH_USERNAME")
SSH_PKEY = os.getenv("SSH_PKEY")
MY_SQL_HOST = os.getenv("MY_SQL_HOST")
MY_SQL_PORT = int(os.getenv("MY_SQL_PORT"))
# DB

DBHOST = os.getenv('DBHOST')
DBUSERNAME = os.getenv('DBUSERNAME')
DBPASSWORD = os.getenv('DBPASSWORD')
DB = os.getenv('DB')


@pytest.fixture()
def set_up_tear_down(page) -> None:
    page.set_viewport_size({"width": 1536, "height": 800})
    page.set_default_timeout(0)
    page.goto(f'{URL_INTERNAL}')
    AP_MYSQL.connect_db()

    yield page

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the subject
    msg['Subject'] = "Automation Report"

    # string to store the body of the mail
    body = "Please find attached report for the automation"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "report.html"
    attachment = open("C:/Users/gupta/Desktop/Automation/playwright/POM_playwright_pytest/products/AdvertisePurple/report.html", "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload(attachment.read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("qashalini0602@gmail.com", "ywgkfxnlpqoexjpq")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail("qashalini0602@gmail.com", "2011guptashalini@gmail.com", text)

    # terminating the session

    s.quit()
    AP_MYSQL.disconnect_db()
    page.close()


@pytest.fixture()
def api_setup() -> None:
    # AP_MYSQL.connect_db()
    verbose = False
    if verbose:
        sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG

    global tunnel
    tunnel = sshtunnel.SSHTunnelForwarder(ssh_address_or_host=(SSH_ADDRESS_OR_HOST, SSH_PORT)
                                          , ssh_username=SSH_USERNAME
                                          , ssh_pkey=SSH_PKEY
                                          , remote_bind_address=(MY_SQL_HOST, MY_SQL_PORT)
                                          )
    tunnel.start()
    global connection
    local_bind_port = 0

    connection = pymysql.connect(
        host=DBHOST,
        user=DBUSERNAME,
        passwd=DBPASSWORD,
        db=DB,
        port=tunnel.local_bind_port
    )
    cur = connection.cursor()
    yield  cur


    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the subject
    msg['Subject'] = "Automation Report - API tests"

    # string to store the body of the mail
    body = "Please find attached report for the API Automation"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "report.html"
    attachment = open("C:/Users/gupta/Desktop/Automation/playwright/POM_playwright_pytest/products/AdvertisePurple/report.html", "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload(attachment.read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("qashalini0602@gmail.com", "ywgkfxnlpqoexjpq")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail("qashalini0602@gmail.com", "2011guptashalini@gmail.com", text)

    # terminating the session

    s.quit()
    connection.close()
    tunnel.close()
    # AP_MYSQL.disconnect_db()
