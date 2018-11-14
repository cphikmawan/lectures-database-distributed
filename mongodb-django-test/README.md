# MongoDB Atlas and Django CRUD Test

#### 05111540000119 - Cahya Putra Hikmawan
##### https://github.com/cphikmawan/database-distributed-courses

### Outline

[1. MongoDB Atlas](#1-mongodb-atlas)

[2. Python Virtual Environment (VEnv)](#2-python-virtual-environment)

[3. Django Deployment](#3-django-deployment)

[4. Testing](#3-deployment-and-testing)

--------------------------------------

### My Device
|||
|---|---|
|OS|Ubuntu 18.04 Dekstop|
|PIP version|18.1 (Using Virtual Env)|
|Python version|3.6 (Using Virtual Env)|

### 1. MongoDB Atlas

- ##### Step 1 - Create Account
    Follow this [video tutorial](https://www.youtube.com/watch?v=-Kmrj6_1rpY&index=2&list=PL4RCxklHWZ9smTpR3hUdq53Su601yCPLj)
    
- ##### Step 2 - Create Cluster
    Follow this [video tutorial](https://www.youtube.com/watch?v=-Kmrj6_1rpY&index=2&list=PL4RCxklHWZ9smTpR3hUdq53Su601yCPLj)

- ##### Step 3 - Create Database User
    Follow this [video tutorial](https://www.youtube.com/watch?v=0Rpu-7vxcdo&index=4&list=PL4RCxklHWZ9smTpR3hUdq53Su601yCPLj)

- ##### Step 4 - IP Whitelist
    Follow this [video tutorial](https://www.youtube.com/watch?v=leNNivaQbDY&list=PL4RCxklHWZ9smTpR3hUdq53Su601yCPLj&index=3)

--------------------------------------

### 2. Python Virtual Environment

- ##### Step 1 - Install Python VEnv
    ```sh
    sudo apt-get install python3-pip
    ```
    ```sh
    sudo pip3 install virtualenv
    ```

- ##### Step 2 - Create VEnv
    ```sh
    virtualenv -p python3 [env_name]
    ```

- ##### Step 3 - Activate VEnv
    ```sh
    cd [env_name]
    source bin/activate
    ```

- ##### Step 4 - Check It
    ```sh
    which pip

    #output
    /home/cloudy/Documents/kuliah/bdt/venv-django/bin/pip
    ```

    ```sh
    which python

    #output
    /home/cloudy/Documents/kuliah/bdt/venv-django/bin/python

    ```
- ##### Step 5 - Install Requirement.txt
    ```sh
    pip install -r requirements.txt
    ```

--------------------------------------

### 3. Django Deployment

- ##### Step 1 - Create Project
    ```sh
    django-admin startproject crudmongodb
    ```

- ##### Step 2 - Connect to Database
    1. Check in MongoDB Atlas website
    2. Select **cluster -> connect -> connection method -> connect your application -> SRV... -> copy -> paste to HOST**

    3. Edit database connection in **settings.py**

        ```sh
        cd crudmongodb
        vim crudmongodb/settings.py
        ```
    4. In this line

        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'djongo',
                'NAME' : 'posts',
                'HOST' : 'mongodb+srv://cloudy:<PASSWORD>@cloudcluster0-tiugx.mongodb.net/test?retryWrites=true'
            }
        }
        ```
    
- ##### Step 3 - Create App
    1. Create

        ```sh
        python manage.py startapp [app_name]
        ```

    2. Activate new App in **settings.py**

        ```python
        INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            '[app_name]',
        ]
        ```

- ##### Step 4 - Make Model
    1. In **model.py** file will look like this

        ```python
        from djongo import models

        class ClassName(models.Model):
            created_on = models.DateTimeField(auto_now_add=True, null=True)
            title = models.CharField(max_length=255)
            text = models.TextField()
        ```

- ##### Step 5 - Make model enable for Admin
    Because we use **Django Administration Template For CRUD Testing**, we need to register **model** to :
    1. In **admin.py** file will look like this
        ```python
        from django.contrib import admin
        from .models import ClassName

        admin.site.register(ClassName)
        ```

- ##### Step 6 - Migration
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```
    > Check MongoDB Atlas Website Collection it will inserted there

- ##### Step 7 - Create Super User
    ```sh
    python manage.py createsuperuser

    Username (leave blank to use 'cloudy'):
    Email address: cp.hikmawan@gmail.com
    Password:
    Password (again):
    Superuser created successfully.
    ```
--------------------------------------

### 4. Testing

- ##### Step 1 - Run Server
    ```sh
    python manage runserver
    ```

- ##### Step 2 - Open http://127.0.0.1:8000/admin/
- ##### Step 3 - Login
- ##### Step 4 - CRUD Testing
- ##### Step 5 - Check in MongoDB Atlas Collection

--------------------------------------
