from pymongo import MongoClient
from bson.json_util import dumps
import json
from bson.objectid import ObjectId

LAN = '192.168.43.49'
Docker_IP = '192.168.99.100'

client = MongoClient(LAN, 1440)
db = client.registrazione
x = db.utenti.find()
y = dumps(x)
utenti = json.loads(y)

users=[]
passwords=[]
emails=[]
ids=[]

for i in range(20):
    a=utenti[i]['_id']['$oid']
    ids.append(str(a))
    x=utenti[i]['user']
    users.append(str(x))
    y=utenti[i]['password']
    passwords.append(str(y))
    z=utenti[i]['email']
    emails.append(str(z))

client = MongoClient(LAN, 1441)
db = client.autenticazione

for i in range(20):
    utente = {"_id": ObjectId(ids[i]),
              "user": users[i],
              "password": passwords[i],
              "email": emails[i],
              "token": ""}
    posts = db.utenti
    post_id = posts.insert_one(utente)
