# Git and GitHub Notes

## Essentipython manage.py runserveral Git Commands

1. **Initialize Git Repository**
   git init
2. # Add Remote Repository -->
git remote add origin https://github.com/your-username/your-repo.git
3. # Stage Files for Commit
git add . 
4. # Commit Changes
git commit -m "Initial commit"
5. # Push Changes to Remote Repository
git push -u origin master
6. # Pull Changes from Remote Repository
git pull origin master
7. # check status
git status

### Handling Large Files
1. # Install Git LFS
git lfs install
2. # Track Large Files with Git LFS
git lfs track "path/to/large/file"
3. # Commit the .gitattributes File
git add .gitattributes
git commit -m "Track large files with Git LFS"

# example of initializing git pushing changes e.gREADME.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/PeterKarym/TradeSphere.git
git push -u origin main

# Virtual environment activate
.\venv\Scripts\activate 

# deactivate Virtual environment
deactivate 

# Virtual environment name
C:\Users\hp\OneDrive\Desktop\DAPP\backend2\venv

# Run Migration Commands
Create Migrations: python manage.py makemigrations
Apply Migrations: python manage.py migrate

# To start your Django development server
PS C:\Users\hp\OneDrive\Desktop\DAPP\backend2>
.\venv\Scripts\activate 
python manage.py makemigrations (ensure connection with the database)
Start the server : python manage.py runserver
browser at http://127.0.0.1:8000/

# To Access the Django Admin Interface(superuser)
.\venv\Scripts\activate 
Start the server : python manage.py runserver
Access the admin interface : http://127.0.0.1:8000/admin/
Username: PeterKarimi
Password: Pk18230161@
Email: peterkarym@gmail.com

# To start your React frontend server
PS C:\Users\hp\OneDrive\Desktop\DAPP\frontend2>
npm start

# To manually establish a websocket connection 
(venv) PS C:\Users\hp\OneDrive\Desktop\DAPP\backend
python websocket_client.py

# PostgreSQL 17 Server
Password:Karimi@254
db name: derivapp_db
db username: postgres
db host: localhost 

# Redis is a Standalone Server running on the local computer to handle communication for Django Channels.
Redis will manage the state and message passing for WebSocket connections. This means that when a WebSocket message is received(eg Signals from EA), Redis ensures that it is correctly routed and handled by the appropriate consumer.
# To start Redis in the command prompt or VS terminal
Path:      cd "C:\Program Files\Redis-7.4.2-Windows-x64-msys2"
           .\redis-server.exe --port 6380

# Check Port Usage in the command prompt you will get its PID(Process id) 
              : netstat -ano | findstr :6380
# Terminate the Redis process using the PID(e.g PID IS 256)
              :taskkill /PID 256 /F
# To Start Daphne(Daphne to runs your ASGI application):
.\venv\Scripts\activate
daphne -p 8080 derivapp.asgi:application
# Test WebSocket Connection with wscat (eg trading websocket url) No virtual environment:
wscat -c ws://localhost:8080/ws/trading/
  test with this message:
  {"signalType": "buy", "price": 1.6789}

# To confirm if Redis is running in its respective port:
     netstat -an | findstr :6380
# To confirm if Daphne is running in its respective port:
     netstat -an | findstr :8080

# To Start the Redis service using NSSM:
  Press Win + X and select Windows PowerShell (Admin)
   :    & "C:\nssm\win64\nssm.exe" start Redis

# monitor the status of the Redis service using NSSM or the Services GUI to ensure it remains running:        
              & "C:\nssm\win64\nssm.exe" status Redis

# Using Redis CLI to check if Redis is running:
              .\redis-cli -p 6380 ping

# Use NSSM commands to stop and start(Restart) the Daphne  service:Administrator command promt
            nssm stop daphne
            nssm start daphne
  
# To insert signal into the database
   .\venv\Scripts\activate
   python insert_signals.py

# How to initiate Django shell
   .\venv\Scripts\activate
   python manage.py shell   