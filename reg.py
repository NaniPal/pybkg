import pymongo
import hashlib
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["garage"]
collection = db["main"]

def index(request):
    return render(request, 'login.html')

# Registration
def register(username, password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    if collection.find_one({'username': username}):
        return 'User already exists'

    collection.insert_one({'username': username, 'password': hashed_password})
    return 'User registered successfully'

# Login
def login(username, password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    user = collection.find_one({'username': username, 'password': hashed_password})
    if user:
        return 'Login successful'
    else:
        return 'Invalid username or password'

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        result = register(username, password)
        return render(request, 'result.html', {'result': result})
    else:
        return HttpResponse('Invalid request method')

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        result = login(username, password)
        return render(request, 'result.html', {'result': result})
    else:
        return HttpResponse('Invalid request method')
