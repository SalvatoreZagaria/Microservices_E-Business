import pymongo
from bson import ObjectId
from flask import Flask
from flask_restful import Resource, Api
from pymongo import MongoClient
import random, string

app = Flask(__name__)
api = Api(app)

LAN = '192.168.43.49'
Docker_IP = '192.168.99.100'


class auth(Resource):
    def get(self, email, password):
        try:
            client = MongoClient(LAN, 1441)
            db = client.autenticazione
            posts = db.utenti
            query_result = posts.find_one({"email": email})
            if query_result:
                if query_result["email"] == email and query_result["password"] == password:
                    letters = string.ascii_lowercase + string.digits
                    token = ''.join(random.choice(letters) for i in range(20))
                    post = {'token': token}
                    try:
                        posts.update_one({'email': email}, {"$set": post}, upsert=False)
                        result = {'result': 'Success', 'token': token, 'user': query_result['user'],
                                  'user_id': str(query_result['_id'])}
                        return result
                    except pymongo.errors.PyMongoError as f:
                        result = {'result': 'Connection error'}
                        return result
                else:
                    result = {'result': 'Credentials error'}
                    return result
            else:
                result = {'result': 'Credentials error'}
                return result
        except pymongo.errors.PyMongoError as e:
            result = {'result': 'Connection error'}
            return result


class create_user(Resource):
    def get(self, user, password, email, id):
        try:
            client = MongoClient(LAN, 1441)
            db = client.autenticazione
            utente = {'_id': ObjectId(id),
                      "user": user,
                      "password": password,
                      "email": email,
                      "token": ""}
            posts = db.utenti
            posts.insert_one(utente)
            result = {'result': 'Success'}
            return result
        except pymongo.errors.PyMongoError as e:
            result = {'result': 'Connection Error'}
            return result


class logout(Resource):
    def get(self, user):
        try:
            client = MongoClient(LAN, 1441)
            db = client.autenticazione
            posts = db.utenti
            query_result = posts.find_one({"user": user})
            if query_result:
                post = {'token': ''}
                posts.update_one({'user': user}, {"$set": post}, upsert=False)
                result = {'result': 'Success'}
                return result
            else:
                result = {'result': 'Fail'}
                return result
        except pymongo.errors.PyMongoError as e:
            result = {'result': 'Connection error'}
            return result


class if_logged(Resource):
    def get(self, token):
        try:
            client = MongoClient(LAN, 1441)
            db = client.autenticazione
            posts = db.utenti
            query_result = posts.find_one({"token": token})
            if query_result:
                result = {'result': 'Success'}
                return result
            else:
                result = {'result': 'Not logged in'}
                return result
        except pymongo.errors.PyMongoError as e:
            result = {'result': 'Connection error'}
            return result


class delete_user(Resource):
    def get(self, id):
        client = MongoClient(LAN, 1441)
        db = client.autenticazione
        posts = db.utenti
        posts.delete_one({'_id': ObjectId(id)})
        result = {'result': 'Success'}
        return result


api.add_resource(auth, '/auth/<email>/<password>')
api.add_resource(create_user, '/new_user/<user>/<password>/<email>/<id>')
api.add_resource(logout, '/logout/<user>')
api.add_resource(if_logged, '/logged/<token>')
api.add_resource(delete_user, '/rollback/<id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
