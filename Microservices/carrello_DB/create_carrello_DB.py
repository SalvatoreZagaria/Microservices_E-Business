from pymongo import MongoClient
from bson.json_util import dumps
import json
from bson.objectid import ObjectId

LAN = '192.168.43.49'
Docker_IP = '192.168.99.100'

client = MongoClient(Docker_IP, 32768)
posts=client.registrazione.utenti
io=posts.find_one({'user':'btbam'})
id_mio=str(io['_id'])

client2 = MongoClient(Docker_IP, 32770)
posts2=client2.catalogo.scarpe
scarpa1=posts2.find_one({'marca':'Nike'})
item={'modello':scarpa1['modello'],
'marca':'Nike',
'taglia':scarpa1['taglie_dispon'][0],
'prezzo':scarpa1['prezzo'],
'quantita':'2',
'id_utente':id_mio,
'id_oggetto':str(scarpa1['_id'])}

client3 = MongoClient(Docker_IP, 32770)
posts3=client3.catalogo.scarpe
scarpa2=posts3.find_one({'marca':'Converse'})
item2={'modello':scarpa2['modello'],
'marca':'Converse',
'taglia':scarpa2['taglie_dispon'][0],
'prezzo':scarpa2['prezzo'],
'quantita':'1',
'id_utente':id_mio,
'id_oggetto':str(scarpa2['_id'])}

client4 = MongoClient(Docker_IP, 32771)
posts4=client4.carrello.items
posts4.insert([item,item2])
