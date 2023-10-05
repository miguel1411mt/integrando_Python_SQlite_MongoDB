from mongoatlas import client
import datetime

DB = client.mydb
collection = DB.mydb_collections

client_bank = [{
    "author": "Miguel da silva",
    "cpf": "12345678901",
    "address": "RJ",
    "type": "Conta corrente",
    "agency": "Itaú",
    "number": "1234",
    "balance": "R$12.000,00",
    "date": datetime.datetime.utcnow()},
    {
        "author": "João medeiros",
        "cpf": "09876543210",
        "address": "SP",
        "type": "Conta corrente",
        "agency": "Santander",
        "number": "0978",
        "balance": "R$34.000,00",
        "date": datetime.datetime.utcnow()},
    {
        "author": "Julia martins",
        "cpf": "24364869701",
        "address": "MG",
        "type": "Conta corrente",
        "agency": "Bradesco",
        "number": "2475",
        "balance": "R$3.000,00",
        "date": datetime.datetime.utcnow()
    }]

Client = DB.Client

insert_client = Client.insert_many(client_bank).inserted_ids

for client in Client.find({}).sort("date"):
    print(client)
