import pymongo
from pymongo import MongoClient
from django.shortcuts import render


client = MongoClient("mongodb://localhost:27017/")
db = client["garage"]
collection = db["main"]

try:
    client = MongoClient("mongodb://localhost:27017/")
    print("MongoDB connection is successful.")
except pymongo.errors.ConnectionFailure as error:
    print(f"Could not connect to MongoDB: {error}")


from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def index(request):
    return render(request, 'login.html')


def send_articles(user, articles):

    if not collection.find_one({'username': user}):
        return 'User does not exist'

    for article in articles:
        collection.insert_one({'user': user, 'article': article})

    return 'Articles sent successfully'


def show_orders():
    orders = collection.find()

    table = []
    for order in orders:
        article = collection.find_one({'name': order['article']})
        table.append([article['car'], article['name'], article['price'], order['user']])

    return table

send_articles('john', ['Article 1', 'Article 2'])

table = show_orders()
for row in table:
    print(row)
