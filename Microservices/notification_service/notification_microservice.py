# coding=utf-8
import pymongo
from flask import Flask
from flask_restful import Resource, Api
from pymongo import MongoClient
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import datetime

app = Flask(__name__)
api = Api(app)

fromaddr = "notification.microservice@gmail.com"
LAN = '192.168.43.49'
Docker_IP = '192.168.99.100'


class new_user(Resource):
    def get(self, email):
        try:
            client = MongoClient(LAN, 1445)
            db = client.notifications
            posts2 = db.event
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            notification = {'event': "Sign up",
                            'timestamp': timestamp,
                            'email': email}
            posts2.insert_one(notification)
        except pymongo.errors.PyMongoError as e:
            result = {'result': 'Connection error'}
            return result
        try:
            toaddr = email
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "Thank you for signing up"

            body = "Dear user,\n\nwe have received your subscription request. Thanks for joining us!\nFeel free to " \
                   "buy your first pair of shoes with us.\n\nCustomer service\n\nThis is an self-generated email. " \
                   "Please don't answer to it. "
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, 'Costanti')
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()
            result = {'result': 'Success'}
            return result
        except smtplib.SMTPException:
            posts2.delete_one(notification)  # ROLLBACK
            result = {'result': 'Connection error'}
            return result


class pagamento(Resource):
    def get(self, email, timestamp):
        try:
            client = MongoClient(LAN, 1445)
            db = client.notifications
            posts2 = db.event
            notification = {'event': "Purchase",
                            'timestamp': timestamp,
                            'email': email}
            posts2.insert_one(notification)
        except pymongo.errors.PyMongoError as e:
            result = {'result': 'Connection error'}
            return result
        try:
            toaddr = email
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "Thank you for purchasing"

            body = "Dear user,\n\nwe have received your purchase request. We will process your request as soon as " \
                   "possible, in order to delegate the shipping to the courier.\nWe will send you the tracking code " \
                   "as soon as possible.\n\nCustomer service\n\nThis is an self-generated email. Please don't answer " \
                   "to it. "
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, "Costanti")
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()
            result = {'result': 'Success'}
            return result
        except smtplib.SMTPException:
            posts2.delete_one(notification)  # ROLLBACK
            result = {'result': 'Connection error'}
            return result


api.add_resource(new_user, '/new_user/<email>')
api.add_resource(pagamento, '/purchase/<email>/<timestamp>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=85)
