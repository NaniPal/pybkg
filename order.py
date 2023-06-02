from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["garage"]
collection = db["main"]

@csrf_exempt
def index(request):
    if request.method == "POST":
        # Get
        name = request.POST.get("name")
        email = request.POST.get("email")
        car = request.POST.get("car")

        # Insert
        collection.insert_one({
            "name": name,
            "email": email,
            "car": car
        })

        return HttpResponse("Order placed successfully!")

    return render(request, "index.html")
