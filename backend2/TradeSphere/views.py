# backend2/TradeSphere/views.py
import logging
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json

logger = logging.getLogger(__name__)

def home(request):
    return HttpResponse("Hello, Django!")

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
        return JsonResponse({'message': 'User registered successfully'})

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                response = JsonResponse({'message': 'User logged in successfully'})
                response.set_cookie('sessionid', request.session.session_key)
                return response
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        else:
            return JsonResponse({'error': 'Username and password required'}, status=400)

@csrf_exempt
def get_user_details(request):
    logger.info(f'User authenticated: {request.user.is_authenticated}, User: {request.user}')
    if request.user.is_authenticated:
        return JsonResponse({'username': request.user.username, 'email': request.user.email})
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

@csrf_exempt
def update_user_details(request):
    if request.method == 'PUT' and request.user.is_authenticated:
        data = json.loads(request.body)
        user = request.user
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        user.save()
        return JsonResponse({'message': 'User details updated successfully'})
    return JsonResponse({'error': 'Not authorized or bad request'}, status=400)
