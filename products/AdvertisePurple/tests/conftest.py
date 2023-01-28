import logging

import pymysql
import pytest
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import sshtunnel
global ENV_NAME

from products.AdvertisePurple.utils import utils as util


@pytest.fixture()
def set_up_tear_down(page) -> None:
    page.set_viewport_size({"width": 1536, "height": 800})
    page.goto(util.URL)
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
    page.close()


@pytest.fixture()
def connect_to_db():
    # Connecting to DB
    verbose = False
    if verbose:
        sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG

    global tunnel
    if ENV_NAME == 'testing':
        tunnel = sshtunnel.SSHTunnelForwarder(ssh_address_or_host=('50.19.142.20', 22)
                                              , ssh_username='ubuntu'
                                              , ssh_pkey='C:/Users/gupta/Desktop/Advertise_Puple/key/ap-db-aws.pem'
                                              , remote_bind_address=('advertise-purple-testing.cihesg5bocgi.us-east-1.rds.amazonaws.com', 3306)
                                              )
    if ENV_NAME == 'staging':
        tunnel = sshtunnel.SSHTunnelForwarder(ssh_address_or_host=('50.19.142.20', 22)
                                              , ssh_username='ubuntu'
                                              , ssh_pkey='C:/Users/gupta/Desktop/Advertise_Puple/key/ap-db-aws.pem'
                                              , remote_bind_address=('advertise-purple-testi23ng.cihesg5bocgi.us-east-1.rds.amazonaws.com', 3306)
                                              )

    tunnel.start()

    global connection
    local_bind_port = 0

    connection = pymysql.connect(
        host='127.0.0.1',
        user='advertise_purple',
        passwd='KXEHncaVuj3Gm76',
        db='advertise_purple',
        port=tunnel.local_bind_port)
    yield connection
    connection.close()
    tunnel.close()
