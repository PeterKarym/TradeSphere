import logging
import asyncio
from django.shortcuts import render, get_object_or_404 
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.conf import settings
from TradeSphere.real_client import real_client_instance  # Import real client instance
from TradeSphere.demo_client import demo_client_instance  # Import demo client instance
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Max
from .models import TradingSignal  # Replace with your actual model name

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
async def request_cashier_info(request):
    if request.method == 'GET':
        try:
            # Directly call the async function
            await real_client_instance.request_cashier_info("deposit", "doughflow", "your_verification_code")
            
            cashier_info = {
                "cashier_name": "Doughflow Cashier",
                "supported_currencies": ["USD", "EUR", "GBP"]
            }
            return JsonResponse(cashier_info)
        except Exception as err:
            logger.error(f"An error occurred while requesting cashier info: {err}")
            return JsonResponse({'error': 'An error occurred'}, status=500)
    else:
        return JsonResponse({"error": 'Invalid request method. Use GET to request cashier info.'}, status=405)
    
@csrf_exempt
def get_cashier_url(request):
    cashier_url = real_client_instance.cashier_url
    logger.info(f"Cashier URL: {cashier_url}")
    if cashier_url:
        return JsonResponse({"cashierURL": cashier_url})
    else:
        logger.error("Cashier URL not available")
        return JsonResponse({'error': 'Cashier URL not available'}, status=500)


# Add Deposit and Withdrawal Views
@csrf_exempt
async def deposit(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = data.get('amount')

        if not amount:
            return JsonResponse({"error": "Amount is required."}, status=400)

        # Directly call the async function
        await real_client_instance.request_deposit(amount)

        return JsonResponse({"message": "Deposit request sent."})
    else:
         return JsonResponse({"error": 'Invalid request method. Use POST to deposit.'}, status=405)
     
@csrf_exempt
async def withdrawal(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        amount = data.get('amount')

        if not email or not amount:
            return JsonResponse({"error": "Email and amount are required."}, status=400)

        # Send withdrawal request via WebSocket client
        await real_client_instance.request_withdrawal(amount, email)

        return JsonResponse({"message": "Withdrawal request sent and verification email triggered. Please verify your email to proceed with the withdrawal."})
    else:
         return JsonResponse({"error": 'Invalid request method. Use POST to withdraw.'}, status=405)

@csrf_exempt
async def handle_email_verification(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        verification_code = data.get('verification_code')

        if not verification_code:
            return JsonResponse({"error": "Verification code is required."}, status=400)

        try:
            # Use the real_client_instance to handle email verification
            await real_client_instance.confirm_email_verification_code(verification_code)

            # Check for an actual response instead of a simulated one
            response_data = await real_client_instance.handle_confirm_email_response(data)

            # Check if the response indicates a successful verification
            if response_data and response_data.get('confirm_email') == 1:
                return JsonResponse({"message": "Email verification successful."}, status=200)
            else:
                error_message = response_data.get('error', 'Email verification failed.')
                return JsonResponse({"error": error_message}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": 'Invalid request method. Use POST to verify email.'}, status=405)
    
 # relay HTTP requests containing trading signals to the WebSocket server

logger = logging.getLogger('trading')

def send_signal(request):
    if request.method == 'GET':  # Use GET since we are fetching signals
        try:
            # Query the latest signal
            latest_signal = TradingSignal.objects.order_by('-timestamp').first()

            if not latest_signal:
                logger.warning("No signals found in the database.")
                return JsonResponse({'status': 'No signals found'}, status=404)

            # Format the signal data (new format: symbol, signalType, price, timestamp)
            signal_data = {
                'symbol': latest_signal.symbol,
                'signalType': latest_signal.signal_type,
                'price': float(latest_signal.price),  # Ensure Decimal is converted to float
                'timestamp': latest_signal.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'formatted_message': f"{latest_signal.symbol}, {latest_signal.signal_type.upper()}, {float(latest_signal.price)}, {latest_signal.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
            }

            logger.info(f"Latest signal retrieved: {signal_data}")

            # Send the signal to the WebSocket group
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'trading_group',
                {
                    'type': 'trading_message',
                    'message': signal_data
                }
            )
            logger.info("Signal broadcasted to WebSocket group: trading_group")

            return JsonResponse({'status': 'Signal sent', 'signal': signal_data})

        except Exception as e:
            logger.error(f"Error processing signal: {e}")
            return JsonResponse({'status': 'Error', 'message': str(e)}, status=500)
    else:
        logger.warning(f"Invalid request method: {request.method}")
        return JsonResponse({'status': 'Invalid request method'}, status=400)
