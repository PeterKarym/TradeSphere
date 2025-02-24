from django.urls import path
from .views import get_account_balances, home, register_user, login_user, get_user_details, update_user_details, request_cashier_info, get_cashier_url, deposit, withdrawal, handle_email_verification

# EndPoints
urlpatterns = [
    path('', home, name='home'),  # Home: http://localhost:8000/
    path('register/', register_user, name='register_user'),  # Register User: http://localhost:8000/api/register/
    path('login/', login_user, name='login_user'),  # Login User: http://localhost:8000/api/login/
    path('user-details/', get_user_details, name='get_user_details'),  # Get User Details: http://localhost:8000/api/user-details/
    path('update-details/', update_user_details, name='update_user_details'),  # Update User Details: http://localhost:8000/api/update-details/
    path('account-balances/', get_account_balances, name='get_account_balances'),  # Account Balances: http://localhost:8000/api/account-balances/
    path('cashier-info/', request_cashier_info, name='request_cashier_info'),  # http://localhost:8000/api/cashier-info/
    path('getCashierURL', get_cashier_url, name='get_cashier_url'),  # Cashier URL: http://localhost:8000/api/getCashierURL
    path('deposit/', deposit, name='deposit'),  # Deposit: http://localhost:8000/api/deposit/
    path('withdrawal/', withdrawal, name='withdrawal'),  # Withdrawal: http://localhost:8000/api/withdrawal/
    path('handle-email-verification/', handle_email_verification, name='handle_email_verification'), # email_verification: http://localhost:8000/api/handle-email-verification/
]
