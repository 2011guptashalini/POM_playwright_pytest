import pytest
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from products.demo_site.utils import utils as util


@pytest.fixture()
def set_up_tear_down(page) -> None:
    page.set_viewport_size({"width": 1536, "height": 800})
    page.goto(util.URL)
    fromaddr = "EMAIL address of the sender"
    toaddr = "EMAIL address of the receiver"

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['qashalini0602@gmail.com'] = fromaddr

    # storing the receivers email address
    msg['2011guptashalini@gmail.com'] = toaddr

    # storing the subject
    msg['Subject'] = "Automation Report"

    # string to store the body of the mail
    body = "Please find attached report for the automation"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "report.html"
    attachment = open("C:/Users/gupta/Desktop/Automation/playwright/POM_playwright_pytest/report.html", "rb")

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
    yield page
