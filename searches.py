from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["garage"]
collection = db["main"]

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def search(request):
    if request.method == 'POST':
        table_name = request.POST.get('table_name')
        results = collection.find({})

        return render(request, 'results.html', {'results': results})
    else:
        return render(request, 'search.html')

def search_results(request):
    keyword = request.GET.get('keyword')
    cars = collection.find({'$or': [
        {'car_mark': {'$regex': keyword, '$options': 'i'}},
        {'car_model': {'$regex': keyword, '$options': 'i'}},
        {'year': {'$regex': keyword, '$options': 'i'}},
        {'color': {'$regex': keyword, '$options': 'i'}},
        {'engine': {'$regex': keyword, '$options': 'i'}}
    ]})

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

