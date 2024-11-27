# Git and GitHub Notes

## Essential Git Commands

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

# Run Migration Commands
python manage.py makemigrations
python manage.py migrate


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

# To start your Django development server
PS C:\Users\hp\OneDrive\Desktop\DAPP\backend2>
.\venv\Scripts\activate 
python manage.py runserver
browser at http://127.0.0.1:8000/

# To Access the Django Admin Interface(superuser)
.\venv\Scripts\activate 
Start the server : python manage.py runserver
Access the admin interface : http://127.0.0.1:8000/admin/
Username: Karimi
Password: Pk18230161@
Email: peterkarym@gmail.com

# To start your React frontend server
PS C:\Users\hp\OneDrive\Desktop\DAPP\frontend2>
npm start
