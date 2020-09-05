import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate


sender_email = "sample@gmail.com"
receiver_email = "sample@gmail.com"
password = input("Type your password and press enter: ")
subject = "Test"

# Create a multipart message and set headers
message = MIMEMultipart()
message["Subject"] = subject
message["From"] = sender_email
message["To"] = receiver_email
message["Bcc"] = receiver_email  # For mass emails
message["date"] = formatdate(localtime=True)

port = 465  # For ssl
smtp_server = "smtp.gmail.com"

# Create the plain-text and HTML version of your message
text = """\
Hi, This is for test.
"""

html = """\
<html>
    <body>
    <p>Hi,<br>
        <h1 style="color:red;">This is for test.</h1>
    </P>
    </body>
</html>
"""

# Turn these into plain/html MIMEText objects
# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
part1 = message.attach(MIMEText(text, "plain"))
part2 = message.attach(MIMEText(html, "html"))

# Open IMAGE file in binary mode
with open('Image Location', 'rb') as image:
    msgImg = MIMEImage(image.read())
    image.close()
    message.attach(msgImg)

# Open PDF file in binary mode
with open('Pdf Location', 'rb') as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    'Content-Disposition',
    f"attachment; filename= {'Pdf Location'}",
)

# Add attachment to message and convert message to string
message.attach(part)
final_message = message.as_string()

# Create secure connection with server and send email
context = ssl.create_default_context()
try:
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(
            sender_email, password
        )

        server.sendmail(
            sender_email, receiver_email, final_message
        )
        print("Email sent.")
except:
    print("Your email can not be sent!")

finally:
    print("Closing the server...")
    server.quit()
