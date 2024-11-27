# a sample script to query the database and print user details:
import os
import django

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'derivapp.settings')
django.setup()

from django.contrib.auth.models import User

# Fetch all users and print their details
users = User.objects.all()
for user in users:
    print(f'Username: {user.username}, Email: {user.email}')

# Fetch a specific user by username
# username = 'example_username'  # Replace with the actual username
# try:
#     user = User.objects.get(username=username)
#     print(f'Username: {user.username}, Email: {user.email}')
# except User.DoesNotExist:
#     print(f'User with username {username} does not exist')
