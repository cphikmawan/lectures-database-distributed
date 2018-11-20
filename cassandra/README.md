# Apache Cassandra CRUD feat Django

#### 05111540000119 - Cahya Putra Hikmawan
##### https://github.com/cphikmawan/database-distributed-courses

### Outline

#### [1. Vagrant](#1-vagrant-and-apache-cassandra)
#### [2. Virtual Env and Django](#2-virtual-env-and-django)
#### [3. Testing](#3-testing)

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
        vb.memory = "1024"
      end

      config.vm.provision "shell", path: "provision/default.sh",    privileged: false
    end
    ```

- ##### Step 2 - Provisioning
    Create script for installing **_Apache Cassandra_** named **default.sh** inside **provision** directory

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
    ```
- ##### Step 3 - Vagrant Up
    ```sh
    $ vagrant up
    ```

#### 2. Virtual Env and Django
#### 3. Testing