import pymongo
from flask import Flask
from flask_restful import Resource, Api
from pymongo import MongoClient
import json
import requests
import time
import datetime

app = Flask(__name__)
api = Api(app)

LAN = '192.168.43.49'
Docker_IP = '192.168.99.100'


class verifica_credito(Resource):
    def get(self, token, id_utente):
        link_to_auth = Docker_IP + ':81'
        link_to_reg = Docker_IP + ':80'
        try:
            conn = requests.get('http://' + link_to_auth + '/logged/' + token, timeout=10)
            if conn.status_code == 200:
                response = json.loads(conn.text)
                if response['result'] == 'Success':
                    try:
                        conn2 = requests.get('http://' + link_to_reg + '/credit/' + id_utente, timeout=10)
                        if conn2.status_code == 200:
                            response = json.loads(conn2.text)
                            if response['result'] == 'Success':
                                credito = response['credit']
                                result = {'result': 'Success',
                                          'credit': str(credito)}
                                return result
                            else:
                                result = {'result': 'Connection error'}
                                return result
                        else:
                            result = {'result': 'Connection error'}
                            return result
                    except requests.exceptions.RequestException as e:
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


class pagamento(Resource):
    def get(self, token, id_utente, importo, email):
        link_to_auth = Docker_IP + ':81'
        link_to_reg = Docker_IP + ':80'
        link_to_notif = Docker_IP + ':85'
        link_to_cart = Docker_IP + ':83'
        try:
            conn = requests.get('http://' + link_to_auth + '/logged/' + token, timeout=10)  # Auth
            if conn.status_code == 200:
                response = json.loads(conn.text)
                if response['result'] == 'Success':
                    try:
                        conn2 = requests.get(
                            'http://' + link_to_reg + '/pagamento/' + id_utente + '/' + importo,
                            timeout=10)  # aggiorna credito
                        if conn2.status_code == 200:
                            response2 = json.loads(conn2.text)
                            if response2['result'] == 'Success':
                                try:
                                    client = MongoClient(LAN, 1444)
                                    db = client.pagamento
                                    ts = time.time()
                                    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                                    acquisto = {"user": id_utente,
                                                "importo": importo,
                                                "timestamp": str(timestamp)}
                                    posts = db.acquisti
                                    posts.insert_one(acquisto)  # scrivi evento su pagamentoDB
                                    try:
                                        conn3 = requests.get(
                                            'http://' + link_to_notif + '/purchase/' + email + '/' + str(
                                                timestamp), timeout=10)  # manda notifica per acquisto
                                        if conn3.status_code == 200:
                                            response3 = json.loads(conn3.text)
                                            if response3['result'] == 'Success':
                                                try:
                                                    conn4 = requests.get(
                                                        'http://' + link_to_cart + '/cart_dele/' + token + '/' + id_utente + '/svuota',
                                                        timeout=10)
                                                    if conn4.status_code == 200:
                                                        response4 = json.loads(conn4.text)
                                                        if response4['result'] == 'Success':
                                                            result = {'result': 'Success'}
                                                            return result
                                                        else:
                                                            result = {'result': 'Success',
                                                                      'warning': 'Cart not emptied'}
                                                            return result
                                                    else:
                                                        result = {'result': 'Success',
                                                                  'warning': 'Cart not emptied'}
                                                        return result
                                                except requests.exceptions.RequestException:
                                                    result = {'result': 'Success',
                                                              'warning': 'Cart not emptied'}
                                                    return result
                                            else:
                                                posts.delete_one(acquisto)  # ROLLBACK
                                                requests.get(
                                                    'http://' + link_to_reg + '/versamento/' + token + '/' + importo + '/' + id_utente)  # ROLLBACK
                                                result = {'result': 'Connection error'}
                                                return result
                                        else:
                                            result = {'result': 'Connection error'}
                                            return result
                                    except requests.exceptions.RequestException as e:
                                        requests.get(
                                            'http://' + link_to_reg + '/versamento/' + token + '/' + importo + '/' + id_utente)  # ROLLBACK
                                        posts.delete_one(acquisto)  # ROLLBACK
                                        result = {'result': 'Connection error'}
                                        return result
                                except pymongo.errors.PyMongoError as e:
                                    requests.get(
                                        'http://' + link_to_reg + '/versamento/' + token + '/' + importo + '/' + id_utente)  # ROLLBACK
                                    result = {'result': 'Connection error'}
                                    return result
                            else:
                                result = {'result': 'Connection error'}
                                return result
                        else:
                            result = {'result': 'Connection error'}
                            return result
                    except requests.exceptions.RequestException as e:
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


api.add_resource(verifica_credito, '/check_credit/<token>/<id_utente>')
api.add_resource(pagamento, '/pagamento/<token>/<id_utente>/<importo>/<email>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=84)
