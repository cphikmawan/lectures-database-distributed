# Apache Cassandra CRUD feat Django

#### 05111540000119 - Cahya Putra Hikmawan
##### https://github.com/cphikmawan/database-distributed-courses

### Outline

#### [1. Vagrant](#1-vagrant-and-apache-cassandra)
#### [2. Virtual Env and Django](#2-virtual-env-and-django)

--------------------------------------

### Prerequisite
| Installed Apps | Version |
| --- | --- |
| OS | Ubuntu 18.04 |
| Vagrant | 18.09.0 |
| Python | 3 |
| PIP | Latest |

--------------------------------------

#### 1. Vagrant and Apache Cassandra
- ##### Step 1 - Vagranfile

    Create **_Vagrantfile_** for create virtual machine, in this case we will create just one node :

    > [Vagrantfile](Vagrantfile)
    ```ruby
    Vagrant.configure("2") do |config|
      config.vm.box = "bento/ubuntu-16.04"
      config.vm.hostname = "cassandra"
      config.vm.network "private_network", ip: "192.168.33.200"
      config.vm.network "public_network", bridge: "enp2s0"

      config.vm.provider "virtualbox" do |vb|
        # Display the VirtualBox GUI when booting the machine
        vb.name = "cassandra"
        vb.gui = false
        # Customize the amount of memory on the VM:
        vb.memory = "2048"
      end

      config.vm.provision "shell", path: "provision/default.sh",    privileged: false
    end
    ```

- ##### Step 2 - Provisioning
    - Create script for installing **_Apache Cassandra_** named **default.sh** inside **provision** directory

        > [default.sh](provision/default.sh)
        ```sh
        #!/bin/bash

        # Referensi
        # https://www.vultr.com/docs/how-to-install-apache-cassandra-3-11-x-on-ubuntu-16-04-lts
        sudo bash -c \\"echo '192.168.33.200 cassandra' >> /etc/hosts\\"

        # sources.list diganti ke kambing.ui.ac.id agar lebih cepat saat download
        sudo cp '/vagrant/sources.list' '/etc/apt/sources.list'
        sudo apt-get update -y

        # Install Open JDK
        sudo apt-get install openjdk-8-jre -y

        # Set $JAVA_HOME di dalam /etc/profile
        sudo bash -c "echo 'JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")'\\" | sudo tee -a /etc/profile
        # Reload environment variable
        source /etc/profile

        # Set repo Cassandra
        bash -c \\"echo 'deb http://www.apache.org/dist/cassandra/debian 311x main'\\" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
        curl https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
        sudo apt-get update

        # Install dan jalankan Cassandra
        sudo apt-get install cassandra -y
        sudo systemctl start cassandra
        sudo systemctl enable cassandra

        sudo cp '/vagrant/provision/cassandra.yaml' '/etc/cassandra/'
        sudo systemctl restart cassandra
        ```

    - Create [cassandra.sh](provision/cassandra.sh)
        ```sh
        sudo cp '/vagrant/provision/cassandra.yaml' '/etc/cassandra/'
        sudo systemctl restart cassandra
        ```

- ##### Step 3 - Vagrant Up
    ```sh
    # dir (cassandra)
    $ vagrant up
    ```

-------------------------------------------------

#### 2. Virtual Env and Django
- ##### Step 1 - Install Virtual Env
    ```sh
    # dir (cassandra)
    $ sudo apt-get install python3-pip
    $ sudo pip3 install virtualenv
    ```

- ##### Step 2 - Create Virtual Env
    ```sh
    # dir (cassandra)
    $ virtualenv -p python3 venv

    # will create venv directory
    ```

- ##### Step 3 - Activate Virtual Env
    ```sh
    # dir (cassandra)
    $ source venv/bin/activate
    ```

- ##### Step 4 - Create Django Project
    ```sh
    # dir (cassandra)
    $ django-admin startproject djangoapp
    ```

- ##### Step 5 - Create Django App
    ```sh
    # dir (cassandra/djangoapp)
    $ python manage.py startapp humans
    ```

- ##### Step 6 - Change Project Ownership
    ```sh
    # dir (cassandra)
    $ sudo chown -R $USER:$USER djangoapp
    ```

- ##### Step 7 - CRUD Development
    1. Edit [settings.py](djangoapp/djangoapp/settings.py)

    2. Edit [models.py](djangoapp/humans/models.py)
        ```python
        import uuid
        from cassandra.cqlengine import columns
        from django_cassandra_engine.models import DjangoCassandraModel

        class Humans(DjangoCassandraModel):
            sr_no = columns.Integer(primary_key=True)
            refund = columns.Text(required=False)
            m_status = columns.Text(required=False)
            income = columns.Text(required=False)
            cheat = columns.Text(required=False)
        ```

    3. Sync Apache Cassandra
        ```sh
        # dir (cassandra)
        $ python manage.py sync_cassandra
        ```
        > It will create keyspace and table automatically

    4. Edit [views.py](djangoapp/humans/views.py)
        ```python
        from django.shortcuts import render, redirect
        from humans.models import Humans
        from django.views.decorators.csrf import csrf_exempt,csrf_protect
        from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

        @csrf_exempt
        def index(request):
            if request.method == 'POST':
                sr_no = request.POST['sr_no']
                refund = request.POST['refund']
                m_status = request.POST['m_status']
                income = request.POST['income']
                cheat = request.POST['cheat']

                human = Humans(sr_no=sr_no)
                human.refund = refund
                human.m_status = m_status
                human.income = income
                human.cheat = cheat
                human.save()

            humans = Humans.objects.all()
            page = request.GET.get('page', 1)

            paginator = Paginator(humans, 5)
            try:
                humans = paginator.page(page)
            except PageNotAnInteger:
                humans = paginator.page(1)
            except EmptyPage:
                humans = paginator.page(paginator.num_pages)

            return render(request, 'index.html', {'humans': humans})

        def add(request):
            return render(request, 'add.html')

        def edit(request, sr_no):
            human = Humans.objects.get(pk=sr_no)

            if request.method == "POST":
                human.refund = request.POST['refund']
                human.m_status = request.POST['m_status']
                human.income = request.POST['income']
                human.cheat = request.POST['cheat']
                human.save()
                return redirect('/')

            return render(request, 'edit.html', {'human': human})

        def delete(request, sr_no):
            human = Humans.objects.get(pk=sr_no)
            human.delete()
            return redirect('/')
        ```

    5. Edit [urls.py](djangoapp/djangoapp/urls.py)
        ```python
        from django.contrib import admin
        from django.urls import path

        from humans import views

        urlpatterns = [
            # path('admin/', admin.site.urls),
            path('', views.index, name='index'),
            path('add/', views.add, name='add'),
            path('edit/<int:sr_no>/', views.edit, name='edit'),
            path('delete/<int:sr_no>/', views.delete, name='delete'),
        ]
        ```

    6. Create [index.html](djangoapp/templates/index.html)
    7. Create [add.html](djangoapp/templates/add.html)
    8. Create [edit.html](djangoapp/templates/edit.html)

- ##### Step 8 - Make Sure Your Directory Tree Like This
        cassandra
        ├── djangoapp
        │   ├── djangoapp
        │   │   ├── settings.py
        │   │   ├── urls.py
        │   │   └── wsgi.py
        │   ├── humans
        │   │   ├── admin.py
        │   │   ├── apps.py
        │   │   ├── migrations
        │   │   ├── models.py
        │   │   ├── tests.py
        │   │   └── views.py
        │   ├── manage.py
        │   └── templates
        │       ├── add.html
        │       ├── edit.html
        │       └── index.html
        ├── provision
        │   ├── cassandra.yaml
        │   ├── default.sh
        │   ├── human.csv
        │   └── requirements.txt
        ├── venv
        ├── README.md
        ├── sources.list
        └── Vagrantfile

- ##### Step 9 - Import Dataset
    ```sh
    # dir (cassandra)
    $ vagrant ssh

    (vagrant)$ cqlsh 192.168.33.200
    ```

    ```sh
    # in vagrant vm
    $ cqlsh 192.168.33.200
    ```
    
    ```sql
    # cassandra shell
    cqlsh> COPY humansdb.Humans (sr_no, refund, m_status, income, cheat) FROM '/vagrant/provision/human.csv' WITH DELIMITER=',' AND HEADER=TRUE ;
    ```

- ##### Final Touch - Run Server
    ```sh
    # dir (cassandra/djangoapp)
    $ python manage.py runserver
    ```

- ##### Testing
    - Try to access http://localhost:8000/ on Browser