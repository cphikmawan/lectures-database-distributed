# MongoDB CRUD with Django feat Docker Container

#### 05111540000119 - Cahya Putra Hikmawan
##### https://github.com/cphikmawan/database-distributed-courses

### Outline

#### [1. Docker and MongoDB Provisioning](#1-docker-and-mongodb-provisioning)
#### [2. Django and Replication](#2-django-and-replication)
#### [3. Testing](#3-testing)

--------------------------------------

### Prerequisite
1.  | Installed Apps | Version |
    | --- | --- |
    | OS| Ubuntu 18.04 |
    | Docker | 18.09.0 |
    | Docker Compose | 1.23.1 |

#### 1. Docker and MongoDB Provisioning
##### Step 1 - Install Docker

[Follow this link](https://docs.docker.com/install/linux/docker-ce/ubuntu/#set-up-the-repository)
    
##### Step 2 - Install Docker Compose

[Follow this link](https://docs.docker.com/compose/install/#install-compose)

> Optional (post install) [Follow this link](https://docs.docker.com/install/linux/linux-postinstall/)

##### Step 3 - Create Directory Structure Like This

    django-crud
    ├── db-manager
    │   ├── data
    │   ├── Dockerfile
    │   └── mongo.conf
    ├── db-node1
    │   └── data
    ├── db-node2
    │   └── data
    ├── db-setup
    │   ├── Dockerfile
    │   ├── replica.js
    │   └── setup.sh
    ├── django-app
    |   └── templates
    ├── docker-compose.yml
    ├── Dockerfile
    └── requirement.txt

```sh
mkdir -p django-crud/db-manager/data
touch django-crud/db-manager/Dockerfile
touch django-crud/db-manager/mongo.conf
mkdir -p django-crud/db-node1/data
mkdir -p django-crud/db-node2/data
mkdir -p django-crud/db-setup
touch django-crud/db-setup/Dockerfile
touch django-crud/db-setup/replica.js
touch django-crud/db-setup/setup.sh
mkdir -p django-crud/django-app/templates
touch django-crud/Dockerfile
touch django-crud/docker-compose.yml
touch django-crud/requirement.txt
```

##### Step 4 - Edit **_Dockerfile_** in Directory "db-manager"

```ruby
FROM mongo

# workdir
WORKDIR /usr/src/configs

# copy config files
COPY mongo.conf .

# define port
EXPOSE 27017

# command
CMD ["--config", "./mongo.conf"]
```

> Initiate db-manager as primary(in first election)
> Will contain mongo.conf

##### Step 5 - Edit **_mongo.conf_** in Directory "db-manager"

```yaml
replication:
    oplogSizeMB: 1024
    replSetName: rs0
```

> Set replica name with rs0

##### Step 6 - Edit **_Dockerfile_** in Directory "db-setup"

```ruby
FROM mongo

# workdir
WORKDIR /usr/src/configs

# install dependency
COPY replica.js .
COPY setup.sh .

RUN ["chmod", "+x", "/usr/local/bin/docker-entrypoint.sh"]
# command
CMD ["./setup.sh"]
```

> For setup the replication

##### Step 7 - Edit **_replica.js_** in Directory "db-setup"

```javascript
rsconf = {
    _id : "rs0",
    members: [
        { _id : 0, host : "db-manager:27017" },
        { _id : 1, host : "db-node1:27017" },
        { _id : 2, host : "db-node2:27017" }
    ]
}

rs.initiate(rsconf);

rs.conf();
```

> Setting replication member and activate

##### Step 8 - Edit **_setup.sh_** in Directory "db-setup"

```sh
#!/usr/bin/env bash

echo ********************
echo Starting Replication
echo ********************

sleep 10 | echo Sleeping...
mongo mongodb://db-manager:27017 replica.js
```

> Bash script for db-manager node to execute the setup replication

##### Step 9 - Edit **_Dockerfile_** in "Main Directory"

```ruby
FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN mkdir django-app
WORKDIR /code/django-app
ADD requirement.txt /code/
RUN pip install -r /code/requirement.txt
ADD ./django-app/ /code/django-app/
```

> Django application deployment

##### Step 10 - Edit **_docker-compose.yml_** in "Main Directory"

```yaml
version: '3'
services:
  db-manager:
    image: "mongo-start"
    build: ./db-manager
    ports:
      - "27017:27017"
    volumes:
      - ./db-manager/data:/data/db
    depends_on:
      - "db-node1"
      - "db-node2"
    
  db-node1:
    image: "mongo"
    command: --replSet rs0 --smallfiles -oplogSize 128
    ports:
      - "27018:27017"
    volumes:
      - ./db-node1/data:/data/db

  db-node2:
    image: "mongo"
    command: --replSet rs0 --smallfiles -oplogSize 128
    ports:
      - "27019:27017"
    volumes:
      - ./db-node2/data:/data/db

  setup-repl:
    image: "setup-repl"
    build: ./db-setup
    depends_on:
      - "db-manager"
  
  # mongocb gui connection
  adminmongo:
    image: "mrvautin/adminmongo"
    ports:
      - "1234:1234"

  # create project
  django-app:
    build: .
    volumes:
      - ./django-app:/code/django-app
    depends_on:
      - "db-manager"

  # create app
  create-app:
    build: .
    command: python3 manage.py startapp myapp
    volumes:
      - ./django-app:/code/django-app
    depends_on:
      - "db-manager"

  # run app
  run-app:
    build: .
    command: python3 manage.py runserver 0.0.0.0:9001
    volumes:
      - ./django-app:/code/django-app
    ports:
      - "9001:9001"
    depends_on:
      - "db-manager"
```

> Provisioning for all nodes

##### Step 11 - Edit **_requirement.txt_** in "Main Directory"

```python
dataclasses==0.6
Django==2.1.3
django-test-addons==1.0
djongo==1.2.30
dnspython==1.15.0
mongoengine==0.16.0
pymongo==3.7.2
pytz==2018.7
six==1.11.0
sqlparse==0.2.4
```

> Requirements for python development

--------------------------------------

#### 2. Django And Replication
##### Step 1 - Install Django & Create Project

```sh
sudo docker-compose run django-app django-admin.py startproject crudapp ./
```

> - Will create project named **"crudapp"** inside django-app directory

##### Step 2 - Run Docker Compose

```sh
sudo docker-compose up
```

> - Will create app named **"myapp"**
> - Run django deployment server at http://localhost:9001

##### Step 3 - Deployment Django CRUD

1.  Change owner
    ```sh
    sudo chown -R $USER:$USER django-app
    ```

2.  Edit several line **_settings.py_** in "crudapp" directory like this
    ```python
    import os
    from mongoengine import connect

    connect(host='mongodb://db-manager/quotesdb?replicaSet=rs0')

    AUTHENTICATION_BACKENDS = (
        'mongoengine.django.auth.MongoEngineBackend',
    )
    .
    .
    .
    INSTALLED_APPS = [
        .
        .
        .
        'myapp',
    ]
    .
    .
    .
    TEMPLATES = [
    {
        .
        .
        'DIRS': [os.path.join( BASE_DIR, 'templates' )],
        .
        .
        .
    ]
    .
    .
    .
    DATABASES = {
        'default': {
            'ENGINE': '',
            'NAME': '',
        }
    }
    .
    .
    .
    ```

3.  Edit **_models.py_** in "myapp" directory like this
    ```python
    from mongoengine import *

    class Quotes(Document):
        Auther = StringField(max_length=200)
        text = StringField(max_length=1000)
    ```

4.  Edit **_views.py_** in "myapp" directory like this
    ```python
    from django.shortcuts import render
    from myapp.models import Quotes
    from django.views.decorators.csrf import csrf_exempt,csrf_protect

    @csrf_exempt
    def index(request):
        if request.method == 'POST':
            # save new post
            Auther = request.POST['Auther']
            text = request.POST['text'] 
            
            quote = Quotes(Auther=Auther)
            quote.text = text
            quote.save()

        # Get all posts from DB
        quotes = Quotes.objects 
        return render(request, 'index.html', {'Quotes': quotes})

    def update(request):
        id = eval("request." + request.method + "['id']")
        quote = Quotes.objects(id=id)[0]
        
        if request.method == 'POST':
            # update field values and save to mongo
            quote.Auther = request.POST['Auther']
            quote.text = request.POST['text']
            quote.save()
            template = 'index.html'
            params = {'Quotes': Quotes.objects} 

        elif request.method == 'GET':
            template = 'update.html'
            params = {'Quotes':quote}
    
        return render(request, template, params)
                                

    def delete(request):
        id = eval("request." + request.method + "['id']")

        if request.method == 'POST':
            quote = Quotes.objects(id=id)[0]
            quote.delete() 
            template = 'index.html'
            params = {'Quotes': Quotes.objects} 
        elif request.method == 'GET':
            template = 'delete.html'
            params = { 'id': id } 

        return render(request, template, params)
    ```

5.  Edit **_urls.py_** in "crudapp" directory like this
    ```python
    from django.contrib import admin
    from django.urls import path

    from myapp import views

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', views.index),
        path('update/', views.update),
        path('delete/', views.delete),
    ]
    ```

6.  Create view templates in "templates" directory

> create html file manually

- [index.html](django-app/templates/index.html)

- [add.html](django-app/templates/add.html)

- [edit.html](django-app/templates/edit.html)

##### Step 4 - Final Touch (Optional)

- After edit get error when access http://localhost:9001, then stop all running docker
    ```sh
    sudo docker system prune -f
    ```

    > Optional, delete all docker image
    > ```sh
    > docker rmi -f $(docker images -a -q)
    > ```

- Run Again
    ```sh
    sudo docker-compose up
    ```

And now you can open the application on http://localhost:9001

--------------------------------------

#### 3. Testing
##### Test Replica Status
```sh
docker exec [docker_name] bash -c 'mongo --eval "rs.status();"'
```

##### Test MongoDB Admin for Accessing DB in Website
- http://localhost:1234
- Create connection to all nodes 
    - mongodb://db-manager
    - mongodb://db-node1
    - mongodb://db-node2

##### Step 1 - Open http://localhost:9001 in Browser
##### Step 2 - CRUD Test
- Basic CRUD Operation

##### Step 3 - Check in Slave Node
- Get in shell docker container
```sh
docker exec -ti [docker_name] /bin/bash
```

- Follow this line (in terminal)
```sh
mongo
```

```sql
rs.slaveOk()
show dbs #for check all database
use db #define db
show collections #check all collection in selected database
db.collectionname.find() #get collection data
```

##### Step 4 - Shutdown Primary Node
```sh
docker stop [docker_name]
```

##### Step 5 - Add New Data
- Basic CRUD Operation

##### Step 6 - Restart Node (The Old Primary Node)
```sh
docker start [docker_name]
```

##### Step 7 - Check Replication Data
- Same with step 3

--------------------------------------
