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


class full_catalog(Resource):
    def get(self, token):
        link_to_auth = Docker_IP + ':81'
        try:
            conn = requests.get('http://' + link_to_auth + '/logged/' + token, timeout=10)
            if conn.status_code == 200:
                response = json.loads(conn.text)
                if response['result'] == 'Success':
                    try:
                        client = MongoClient(LAN, 1442)
                        db = client.catalogo
                        posts = db.scarpe
                        cursor = posts.find({})
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


api.add_resource(full_catalog, '/catalog/<token>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=82)
