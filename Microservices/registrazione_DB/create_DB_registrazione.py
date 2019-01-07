from faker import Faker
import random
from pymongo import MongoClient

fake = Faker()
LAN = '192.168.43.49'
Docker_IP = '192.168.99.100'

nomi=[]
users=[]
passwords=[]
emails=[]
credit=[]

for i in range(20):
    nomi.append(str(fake.name()))
    users.append(str(fake.user_name()))
    passwords.append(str(fake.password(special_chars=True, digits=True, upper_case=True, lower_case=True)))
    #mongo crea un objectID in automatico
    emails.append(str(fake.email()))
    credit.append(random.randint(1,500))

client = MongoClient(LAN, 1440) 
db = client.registrazione

for i in range(20):
    utente = {"name": nomi[i],
        "user": users[i],
        "password": passwords[i],
        "email": emails[i],
        "credit": credit[i]}
    posts = db.utenti
    post_id = posts.insert_one(utente)
