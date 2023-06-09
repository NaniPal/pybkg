import smtplib
import pymongo
from pymongo import MongoClient
from django.shortcuts import render

client = MongoClient("mongodb://localhost:27017/")
db = client["garage"]
collection = db["main"]

def index(request):
    #pull
    emails = [doc["email"] for doc in collection.find({}, {"email": 1})]

    # sender
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login("dream.garage@gmail.com", "password")

        for email in emails:
            message = "Some random stuff"
            smtp.sendmail("dream.garage@gmail.com", email, message)

        smtp.quit()

    return render(request, 'index.html')
