from email.mime.multipart import MIMEMultipart
from flask import Flask, request, render_template
import smtplib
from email.mime.text import MIMEText

from werkzeug.utils import send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("CustomInterface.html")

@app.route("/submit-form", methods=["POST"])
def submit_form():
    name = request.form.get("name")
    user_email = request.form.get("email")
    id_number = request.form.get("n-number")
    message = request.form.get("message")

    try:
        send_email(name, user_email, id_number, message)
        return f"""
        <html>
            <head>
                <meta http-equiv="refresh" content="10;url=/"  />
                <title>Thank You!</title>
            </head>
            <body>
                <h1>Thank You, {name}! Your message has been sent to Scott Piersall.</h1>
                <p>You will be redirected to the Hompage in 10 seconds.</p>
            </body>
        </html>
        """
    except Exception as e:
        return f"Failed to Send Email. Error: {str(e)} "

def send_email(name, user_email, id_number, message):
    sender_email = "scottshelpbox@gmail.com"
    sender_password = "whps uykc pcko tceu"
    receiver_email = "scott.piersall@unf.edu"

    subject = f"New message from {name}"
    body = f"""
    Name: {name}
    Email: {user_email}
    N-number: {id_number}
    
    Message: 
    {message}
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

if __name__ == "__main__":
    app.run(debug=True)
