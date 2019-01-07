import pymongo
from flask import Flask
from flask_restful import Resource, Api
from pymongo import MongoClient
import json
import requests

app = Flask(__name__)
api = Api(app)

LAN = '192.168.43.49'
Docker_IP = '192.168.99.100'


class insert(Resource):
    def get(self, modello, marca, taglia, prezzo, id_utente, id_oggetto, quantita, token):
        link_to_auth = Docker_IP + ':81'
        try:
            conn = requests.get('http://' + link_to_auth + '/logged/' + token, timeout=10)
            if conn.status_code == 200:
                response = json.loads(conn.text)
                if response['result'] == 'Success':
                    try:
                        client = MongoClient(LAN, 1443)
                        db = client.carrello
                        item = {"modello": modello,
                                "marca": marca,
                                "taglia": float(int(taglia)),
                                "prezzo": float(int(prezzo)),
                                "id_utente": id_utente,
                                "id_oggetto": id_oggetto,
                                "quantita": float(int(quantita))}
                        posts = db.items
                        posts.insert_one(item)
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


class retrieve(Resource):
    def get(self, token, id_utente):
        link_to_auth = Docker_IP + ':81'
        try:
            conn = requests.get('http://' + link_to_auth + '/logged/' + token, timeout=10)
            if conn.status_code == 200:
                response = json.loads(conn.text)
                if response['result'] == 'Success':
                    try:
                        client = MongoClient(LAN, 1443)
                        db = client.carrello
                        posts = db.items
                        cursor = posts.find({"id_utente": id_utente})
                        result = []
                        for doc in cursor:
                            result.append(doc)
                        for i in range(len(result)):
                            result[i]['_id'] = str(result[i]['_id'])
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


class delete(Resource):
    def get(self, token, id_utente, id_oggetto):
        link_to_auth = Docker_IP + ':81'
        try:
            conn = requests.get('http://' + link_to_auth + '/logged/' + token, timeout=10)
            if conn.status_code == 200:
                response = json.loads(conn.text)
                if response['result'] == 'Success':
                    try:
                        client = MongoClient(LAN, 1443)
                        db = client.carrello
                        posts = db.items
                        if id_oggetto == "svuota":
                            posts.delete_many({"id_utente": id_utente})
                        else:
                            posts.delete_many({"id_utente": id_utente,
                                               "id_oggetto": id_oggetto})
                        result = {'result': 'Success'}
                        return result
                    except pymongo.errors.PyMongoError as e:
                        result = {'result': 'Connection error'}
                        return result
                else:
                    result = {'result': 'Not logged in'}
                    return json.dumps(result)
            else:
                result = {'result': 'Connection error'}
                return result
        except requests.exceptions.RequestException as e:
            result = {'result': 'Connection error'}
            return result


api.add_resource(insert, '/cart_insert/<modello>/<marca>/<taglia>/<prezzo>/<id_utente>/<id_oggetto>/<quantita>/<token>')
api.add_resource(retrieve, '/cart_retr/<token>/<id_utente>')
api.add_resource(delete, '/cart_dele/<token>/<id_utente>/<id_oggetto>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=83)
