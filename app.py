import pymongo
from pymongo import MongoClient
from django.shortcuts import render
from django.http import HttpResponse

client = MongoClient("mongodb://localhost:27017/")
db = client["garage"]
collection = db["main"]

try:
    client = MongoClient("mongodb://localhost:27017/")
    print("MongoDB connection is successful.")
except pymongo.errors.ConnectionFailure as error:
    print(f"Could not connect to MongoDB: {error}")

def index(request):
    return render(request, 'index.html')

def search(request):
    keyword = request.GET.get('keyword')
    cars = collection.find({
        '$or': [
            {'car_mark': {'$regex': keyword, '$options': 'i'}},
            {'car_model': {'$regex': keyword, '$options': 'i'}},
            {'year': {'$regex': keyword, '$options': 'i'}},
            {'color': {'$regex': keyword, '$options': 'i'}},
            {'engine': {'$regex': keyword, '$options': 'i'}}
        ]
    })
    results = []
    for car in cars:
        results.append({
            'car_mark': car['car_mark'],
            'car_model': car['car_model'],
            'year': car['year'],
            'color': car['color'],
            'engine': car['engine']
        })
    return render(request, 'result.html', {'results': results})

