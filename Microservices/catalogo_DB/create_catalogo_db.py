from pymongo import MongoClient
import random


LAN = '192.168.43.49'
Docker_IP = '192.168.99.100'

marche = ['Nike', 'Adidas', 'Puma', 'Converse']
modelli = ['Roshe Sneaker Unisex', 'Nike Tanjun GS bambino', 'Nike Hypervenom Phelon Scarpe White Game',
           'Nike performancestadium',
           'Tubular Shadow Scarpe Ginnastica', 'Superstar Scarpe Ginnastica', 'Superstar Scarpe Sportive Unisex',
           'Tubular Ginnastica Unisex Adulto footwear',
           'Puma Suede Heart Satin Donna Sneaker Nero', 'Puma Vikky Platform Donna', 'Puma Ignite Evoknit Unisex',
           'Puma Enzo Mesh Uomo',
           'M9613c Unisex', 'All Star Hi Canvas Unisex', 'Ct Core Lea Hi Unisex', 'Chuck Taylor All Star Unisex']
img = []

client = MongoClient(Docker_IP, 32770)
db = client.catalogo

f = open('C:\\users\\szaga\\Google Drive\\Poliba\\Magistrale Informatica\\Advanced software '
         'engineering\\Progetto\Progetto_Microservices\\catalogo_DB\\Immagini\\link.txt', 'r')
x = f.read()
y = x.splitlines()
x = y[17:33]

for i in range(len(modelli)):
    taglie = random.sample(range(36, 48), 5)
    prezzo = random.randint(75, 125)

    if i < 4:
        marca = marche[0]
    elif i >= 4 and i < 8:
        marca = marche[1]
    elif i >= 8 and i < 12:
        marca = marche[2]
    else:
        marca = marche[3]

    scarpa = {"marca": marca,
              "modello": modelli[i],
              "taglie_dispon": taglie,
              "prezzo": prezzo,
              "immagine": x[i]}
    posts = db.scarpe
    post_id = posts.insert_one(scarpa)
