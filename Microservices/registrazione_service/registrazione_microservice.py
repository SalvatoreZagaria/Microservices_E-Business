import pymongo
from flask import Flask
from flask_restful import Resource, Api
from pymongo import MongoClient
import json
import requests
from bson import ObjectId

app = Flask(__name__)
api = Api(app)

LAN = '192.168.43.49'
Docker_IP = '192.168.99.100'


class create_user(Resource):
    def get(self, nome, user, password, email, credito):
        global utente, posts
        error = False
        try:
            client = MongoClient(LAN, 1440)
            db = client.registrazione
            utente = {"name": nome,
                      "user": user,
                      "password": password,
                      "email": email,
                      "credit": credito}
            posts = db.utenti
            checkUser = posts.find_one({'user': user})
            checkMail = posts.find_one({'email': email})
            if checkMail or checkUser:
                result = {'result': 'Credentials already exist'}
                return json.dumps(result)
            else:
                ID = posts.insert_one(utente).inserted_id
        except pymongo.errors.PyMongoError as e:
            error = True

        link_to_auth = Docker_IP + ':81'
        # delegate Autenticazione to create new user in its database
        try:
            conn = requests.get(
                'http://' + link_to_auth + '/new_user/' + user + '/' + password + '/' + email + '/' + str(ID),
                timeout=10)
            try:
                response = json.loads(conn.text)
            except ValueError:
                response = {'result': 'Fail'}
            if conn.status_code != 200 or response['result'] != 'Success':
                error = True
                posts.delete_one(utente)  # ROLLBACK
        except requests.exceptions.RequestException as e:
            posts.delete_one(utente)  # ROLLBACK
            error = True

        link_to_notification = Docker_IP + ':85'

        try:
            if error==False:
                conn2 = requests.get('http://' + link_to_notification + '/new_user/' + email,
                                     timeout=10)  # Manda notifica registrazione
                if conn2.status_code != 200:
                    posts.delete_one(utente)  # ROLLBACK
                    requests.get(
                        'http://' + link_to_auth + '/rollback/' + str(ID), timeout=10)
                    error = True
        except requests.exceptions.RequestException as e:
            posts.delete_one(utente)  # ROLLBACK
            requests.get(
                'http://' + link_to_auth + '/rollback/' + str(ID))
            error = True
        if error:
            result = {'result': 'Connection error'}
            return result
        else:
            result = {'result': 'Success'}
            return result


class versamento(Resource):
    def get(self, token, credito, id_utente):
        link_to_auth = Docker_IP + ':81'
        try:
            conn = requests.get('http://' + link_to_auth + '/logged/' + token, timeout=10)
            if conn.status_code == 200:
                response = json.loads(conn.text)
                if response['result'] == 'Success':
                    try:
                        client = MongoClient(LAN, 1440)
                        db = client.registrazione
                        posts = db.utenti
                        user = posts.find_one({'_id': ObjectId(id_utente)})
                        credit = user['credit']
                        credit = int(float(credit))
                        new_credit = credit + int(float(credito))
                        post = {'credit': str(new_credit)}
                        posts.update_one({'_id': ObjectId(id_utente)}, {"$set": post}, upsert=False)
                        result = {'result': 'Success'}
                        return result
                    except pymongo.errors.PyMongoError as e:
                        result = {'result': 'Connection error'}
                        return result
                else:
                    result = {'result': 'Not logged in'}
                    return result
            else:
                result = {'result': 'Connection error'}
                return result
        except requests.exceptions.RequestException as e:
            result = {'result': 'Connection error'}
            return result


class send_credit(Resource):
    def get(self, id_utente):
        try:
            client = MongoClient(LAN, 1440)
            db = client.registrazione
            posts = db.utenti
            user = posts.find_one({"_id": ObjectId(id_utente)})
            credito = user['credit']
            result = {'result': 'Success',
                      'credit': str(credito)}
            return result
        except pymongo.errors.PyMongoError as e:
            result = {'result': 'Connection error'}
            return result


class update_credit(Resource):
    def get(self, id_utente, importo):
        try:
            client = MongoClient(LAN, 1440)
            db = client.registrazione
            posts = db.utenti
            user = posts.find_one({'_id': ObjectId(id_utente)})
            credit = user['credit']
            credit = int(float(credit))
            new_credit = credit - int(float(importo))
            post = {'credit': str(new_credit)}
            posts.update_one({'_id': ObjectId(id_utente)}, {"$set": post}, upsert=False)
            result = {'result': 'Success'}
            return result
        except pymongo.errors.PyMongoError as e:
            result = {'result': 'Connection error'}
            return result


api.add_resource(create_user, '/new_user/<nome>/<user>/<password>/<email>/<credito>')
api.add_resource(versamento, '/versamento/<token>/<credito>/<id_utente>')
api.add_resource(send_credit, '/credit/<id_utente>')
api.add_resource(update_credit, '/pagamento/<id_utente>/<importo>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
