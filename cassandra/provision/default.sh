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