import pymongo as pyM
import datetime
import pprint

# client
client = pyM.MongoClient('mongodb+srv://heitorcesarino:vkMqqY3uWAxP76Cs@cluster0.4nxopdg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

#db
db = client.bank
customer_collection = db.customer_collection
account_collection = db.account_collection

customer = {
    "nome":"frodo",
    "cpf":"12345678900",
    "endereco":"condado 123",
}

customer_id = customer_collection.insert_one(customer).inserted_id
print(customer_id)


account = {
    "tipo":"conta corrente",
    "agencia":"5050",
    "num":"3245671",
    "id_customer":"1",
    "saldo":"23345.98",
}

account_id = account_collection.insert_one(account).inserted_id
print(account_id)

pprint.pprint(db.customer_collection.find_one())