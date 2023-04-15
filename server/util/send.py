import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


def sendEmail(sender, password, subject, receivers, content, image_path=None):
    """This method sends an email about the label to modify to the experts."""
    # Use smtp protocol to send
    smtpHost = 'smtp.office365.com'
    smtpPort = 587
    # Add the From: and To: headers at the start!
    # email information and content settings
    message_text = MIMEText(content)
    message = MIMEMultipart('related')
    message['Subject'] = subject  # Email subject info
    message['From'] = sender      # Sender info
    message['To'] = receivers[0]  # Receiver info

    if image_path != None:
        pic = open(image_path, "rb")
        img = MIMEImage(pic.read())
        img.add_header('Content-ID', '<image1>')
        pic.close()
        message.attach(img)
    message.attach(message_text)
    try:
        smtpObj = smtplib.SMTP(smtpHost, smtpPort)
        # smtpObj.set_debuglevel(1)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(sender, password)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print("Successfully sent email")
    except smtplib.SMTPException:
        print("Error: unable to send email")

# sendEmail(sender='recktabcd@outlook.com',
#           password="ausualpw",
#           subject="Training Result",
#           receivers=['wengxili@umich.com'],
#           content="<h1>Hello World</h1>")