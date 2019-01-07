from flask import Flask
from flask_restful import Resource, Api
import requests

LAN = '192.168.43.49'
Docker_IP = '192.168.99.100'

link_to_auth = Docker_IP + ':81'
link_to_reg = Docker_IP + ':80'
link_to_cat = Docker_IP + ':82'
link_to_paga = Docker_IP + ':84'
link_to_cart = Docker_IP + ':83'

app = Flask(__name__)
api = Api(app)


class Autenticazione(Resource):
    def get(self, email, password):
        conn = requests.get('http://' + link_to_auth + '/auth/' + email + '/' + password, timeout=10)
        if conn.status_code == 200:
            return conn.text
        else:
            result = {'result': 'Connection error'}
            return result


class Autenticazione_for_logout(Resource):
    def get(self, user):
        conn = requests.get('http://' + link_to_auth + '/logout/' + user, timeout=10)
        if conn.status_code == 200:
            return conn.text
        else:
            result = {'result': 'Connection error'}
            return result


class Registrazione(Resource):
    def get(self, nome, user, password, email, credito):
        conn = requests.get(
            'http://' + link_to_reg + '/new_user/' + nome + '/' + user + '/' + password + '/' + email + '/' + credito,
            timeout=10)
        if conn.status_code == 200:
            return conn.text
        else:
            result = {'result': 'Connection error'}
            return result


class Registrazione_versamento(Resource):
    def get(self, token, credito, id_utente):
        conn = requests.get('http://' + link_to_reg + '/versamento/' + token + '/' + credito + '/' + id_utente,
                            timeout=10)
        if conn.status_code == 200:
            return conn.text
        else:
            result = {'result': 'Connection error'}
            return result


class Catalogo(Resource):
    def get(self, token):
        conn = requests.get('http://' + link_to_cat + '/catalog/' + token, timeout=None)
        if conn.status_code == 200:
            return conn.text
        else:
            result = {'result': 'Connection error'}
            return result


class Carrello_ins(Resource):
    def get(self, modello, marca, taglia, prezzo, id_utente, id_oggetto, quantita, token):
        conn = requests.get(
            'http://' + link_to_cart + '/cart_insert/' + modello + '/' + marca + '/' + taglia + '/' + prezzo + '/' + id_utente + '/' + id_oggetto + '/' + quantita + '/' + token, timeout=10)
        if conn.status_code == 200:
            return conn.text
        else:
            result = {'result': 'Connection error'}
            return result


class Carrello_retr(Resource):
    def get(self, token, id_utente):
        conn = requests.get('http://' + link_to_cart + '/cart_retr/' + token + '/' + id_utente, timeout=10)
        if conn.status_code == 200:
            return conn.text
        else:
            result = {'result': 'Connection error'}
            return result


class Carrello_dele(Resource):
    def get(self, token, id_utente, id_oggetto):
        conn = requests.get('http://' + link_to_cart + '/cart_dele/' + token + '/' + id_utente + '/' + id_oggetto,
                            timeout=10)
        if conn.status_code == 200:
            return conn.text
        else:
            result = {'result': 'Connection error'}
            return result


class Pagamento_verifica_credito(Resource):
    def get(self, token, id_utente):
        conn = requests.get('http://' + link_to_paga + '/check_credit/' + token + '/' + id_utente, timeout=10)
        if conn.status_code == 200:
            return conn.text
        else:
            result = {'result': 'Connection error'}
            return result


class Pagamento(Resource):
    def get(self, token, id_utente, importo, email):
        conn = requests.get(
            'http://' + link_to_paga + '/pagamento/' + token + '/' + id_utente + '/' + importo + '/' + email,
            timeout=10)
        if conn.status_code == 200:
            return conn.text
        else:
            result = {'result': 'Connection error'}
            return result


api.add_resource(Autenticazione, '/auth/<email>/<password>')
api.add_resource(Autenticazione_for_logout, '/logout/<user>')
api.add_resource(Registrazione, '/register/<nome>/<user>/<password>/<email>/<credito>')
api.add_resource(Registrazione_versamento, '/versamento/<token>/<credito>/<id_utente>')
api.add_resource(Catalogo, '/catalog/<token>')  # ok
api.add_resource(Carrello_ins, '/cart_insert/<modello>/<marca>/<taglia>/<prezzo>/<id_utente>/<id_oggetto>/<quantita'
                               '>/<token>')
api.add_resource(Carrello_retr, '/cart_retr/<token>/<id_utente>')
api.add_resource(Carrello_dele, '/cart_dele/<token>/<id_utente>/<id_oggetto>')
api.add_resource(Pagamento_verifica_credito, '/check_credit/<token>/<id_utente>')
api.add_resource(Pagamento, '/pagamento/<token>/<id_utente>/<importo>/<email>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=86)
