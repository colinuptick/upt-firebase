from pymongo.mongo_client import MongoClient
import pymongo

cluster = MongoClient("mongodb+srv://colin:Momy1234@cluster0.1zmkjho.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = cluster['Company_Q']
collection = db['tickets']

ticket = {
    'team': 'Indiana Fever',
    'date': '5/3/25',
    'section': '204',
    'seat': 'H12-15',
    'tag': ['manager', 'scrub']
}

collection.insert_one(ticket)
print('success')