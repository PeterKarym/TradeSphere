import logging
import asyncio
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.conf import settings
from TradeSphere.real_client import real_client_instance  # Import demo client instance
from TradeSphere.demo_client import demo_client_instance  # Import demo client instance

logger = logging.getLogger(__name__)


def home(request):
    return HttpResponse("Hello, Django!")

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
        return JsonResponse({'message': 'User registered successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method. Use POST to register.'}, status=405)

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
    else:
        return JsonResponse({'error': 'Invalid request method. Use POST to login.'}, status=405)

@csrf_exempt
def get_user_details(request):
    logger.info(f'User authenticated: {request.user.is_authenticated}, User: {request.user}')
    if request.method == 'GET':
        if request.user.is_authenticated:
            return JsonResponse({'username': request.user.username, 'email': request.user.email})
        else:
            return JsonResponse({'error': 'User not authenticated'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method. Use GET to fetch user details.'}, status=405)

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
    elif request.method == 'GET':
        return JsonResponse({'error': 'Invalid request method. Use PUT to update user details.'}, status=405)
    else:
        return JsonResponse({'error': 'Not authorized or bad request'}, status=400)

@csrf_exempt
def get_account_balances(request):
    with real_client_instance.balance_lock:
        real_accounts = real_client_instance.balances
        total_real_assets_balance = sum(real_accounts.values())

    with demo_client_instance.balance_lock:
        demo_accounts = demo_client_instance.balances
        total_demo_assets_balance = sum(demo_accounts.values())

    logger.info(f'Real Accounts in view: {real_accounts}, Total Real Assets Balance: {total_real_assets_balance}')
    logger.info(f'Demo Accounts in view: {demo_accounts}, Total Demo Assets Balance: {total_demo_assets_balance}')

    data = {
        'real_accounts': real_accounts,
        'demo_accounts': demo_accounts,
        'total_real_assets_balance': total_real_assets_balance,
        'total_demo_assets_balance': total_demo_assets_balance
    }
    return JsonResponse(data)

@csrf_exempt
def request_cashier_info(request):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(real_client_instance.request_cashier_info("deposit", "doughflow", "your_verification_code"))
        
        cashier_info = {
            "cashier_name": "Doughflow Cashier",
            "supported_currencies": ["USD", "EUR", "GBP"]
        }
        return JsonResponse(cashier_info)
    except Exception as err:
        logger.error(f"An error occurred while requesting cashier info: {err}")
        return JsonResponse({'error': 'An error occurred'}, status=500)

@csrf_exempt
def get_cashier_url(request):
    cashier_url = real_client_instance.cashier_url
    logging.info(f"Cashier URL: {cashier_url}")
    if cashier_url:
        return JsonResponse({"cashierURL": cashier_url})
    else:
        logging.error("Cashier URL not available")
        return JsonResponse({'error': 'Cashier URL not available'}, status=500)
