import smtplib
import ssl
import json

with open('email.txt') as json_file:
    data = json.load(json_file)
    sender_email = data["email"]
    password = data["pass"]

port = 465
message = """\
Subject: Ich habe einen Deal gesichert!

Ich habe gerade diesen Artikel gesichert:

"""
message_cb = """

Bestellen kannst du bis:

"""

def send_email(Artikel, Zeit, User):
    Artikel = Artikel.replace("ä", "ae")
    Artikel = Artikel.replace("ü", "ue")
    Artikel = Artikel.replace("ö", "oe")
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, User, message + str(Artikel) + message_cb + str(Zeit))