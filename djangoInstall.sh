#! /bin/sh

# Prerequisites
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install python python-dev python-pip -y
sudo apt-get install git -y

# Django
sudo pip install django

# PostgreSQL & postgis for spacial data
cd ~/Downloads
wget http://download.osgeo.org/postgis/source/postgis-2.0.3.tar.gz
tar xzf postgis-2.0.3.tar.gz
cd postgis-2.0.3
sudo ./configure
sudo make
sudo make install
cd ~/Downloads
wget http://postgis.net/stuff/postgis-2.1.4dev.tar.gz
tar -xvzf postgis-2.1.4dev.tar.gz
cd postgis-2.1.4dev
sudo ./configure
sudo make
sudo make install
cd ~
sudo apt-get install binutils libgdal-dev gdal-bin -y
sudo apt-get install libgdal1-dev -y
sudo apt-get install postgresql-9.3 postgresql-contrib-9.3  postgresql-server-dev-9.3 -y
sudo apt-get install postgresql-9.3-postgis-2.0 -y
sudo apt-get install python-psycopg2 -y
sudo apt-get install pgadmin3 -y
# enter shell
#    sudo -u postgres psql postgres
# set password
#    \password postgres
# ctrl+z to exit shell
# create db
#    sudo -u postgres createdb mydb;
# setup
#    sudo -u postgres psql
#    CREATE EXTENSION adminpack;
# restart
#    sudo service postgresql restart

# Apache
sudo apt-get install apache2 libapache2-mod-wsgi -y
# configure apache
#    sudo vim /etc/apache2/httpd.conf
# add
#    Alias /static/ /home/ubuntu/composersCouch/composersCouch/static/

#    <Directory /home/ubuntu/composersCouch/composersCouch/static>
#    Order deny,allow
#    Allow from all
#    </Directory>

#    WSGIScriptAlias / /home/ubuntu/composersCouch/composersCouch/apache/django.wsgi


# pillow image support
sudo apt-get install libjpeg-dev -y
sudo apt-get install libjpeg62 libjpeg62-dev zlib1g-dev -y

# install redis server
sudo apt-get install redis -y
sudo apt-get install redis-server -y

# install memcached
sudo apt-get install memcached -y

# install Less
sudo apt-get install python-software-properties python g++ make -y
sudo add-apt-repository ppa:chris-lea/node.js -y
sudo apt-get update -y
sudo apt-get install nodejs -y
sudo apt-get install npm -y
sudo npm install -g less


exit 0
