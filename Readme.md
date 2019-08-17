Backend Server for Calorie Tracker App:

Following REST Api endpoints are exposed by the server:

CREATE/ READ/ UPDATE/ DELETE (USERS)

-- /user/create/

-- /user/get/  (Filtering functionality available)

-- /user/update

-- /user/delete/

CREATE/ READ/ UPDATE/ DELETE (TRACKER RECORDS)

-- /entry/create/

-- /entry/get/ (Filtering functionality available)

-- /entry/update/

-- /entry/delete/

AUTHENTICATION

-- /api/token/

-- /api/token/refresh/

Each API calls needs to be authenticated with a JWT Token which can be retrieved by calling the above api endpoint.


For seting up the server follow below steps:

Install pip3 (for OSX: https://vgkits.org/blog/pip3-macos-howto/)

Install virtualenv (for OSX: https://sourabhbajaj.com/mac-setup/Python/virtualenv.html)

Create a virtualenv with command: virtualenv calorieTracker (you can name it as you like)

Enter the virtual environment directory: cd calorieTracker

Activate virtual environment: source bin/activate

clone the calorie tracker repo: clone 

Go To Project Root: cd calorieTracker

Install required dependencies: pip3 install -r requirements.txt

Make Migrations: python3 manage.py makemigrations

Migrate: python3 manage.py migrate

Run Server: python3 manage.py runserver

You should have a server up and running on your localhost at Port 8000

-- Creating Superuser
Create a new user by calling the following endpoint:  /user/create/ with type as admin.
Then  Go to localhost:8000/admin on browser and you should be able to login as admin