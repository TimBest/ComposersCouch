Django powered site for composers couch


Setting development to true
    add 'DEVELOPMENT=True' to the end of ~/.bashrc
    add 'export DEVELOPMENT=Treu' to the end of ~/.profile
    load with source ~/.bashrs and ~/.profile respectivly

SSH into production server
    ssh -i djangosite-eb.pem ec2-user@54.152.14.2
    /opt/python/current/app/
    /opt/python/run/venv/bin/activate

    scp -i CCkey.pem -r composersCouch ubuntu@54.200.80.27:/home/ubuntu

dev server:
    sudo gedit /etc/hosts
    add '127.0.0.1        dev.composerscouch.com' as the first line

Create database user
    sudo su postgres -c psql
        ALTER USER postgres WITH PASSWORD 'YourPassword';
        \q
    sudo passwd -d postgres
    sudo su postgres -c passwd
    sudo su postgres -c psql
        create database composersCouchdb;
        grant all privileges on database composersCouchdb to postgres;
        CREATE EXTENSION postgis;
        \q
    sudo service postgresql restart
    sudo ldconfig

Load Location Data:
    python manage.py shell
        from contact import load
        load.run()

Load Genre Data:
    python manage.py shell
        from genres import load
        load.run()

Test Emails:
    python -m smtpd -n -c DebuggingServer localhost:1025

Setup AWS instance:
    sudo su -
    yum update -y
    yum install -y python-devel libpcap libpcap-devel libnet libnet-devel pcre pcre-devel gcc gcc-c++ libtool make libyaml libyaml-devel binutils libxml2 libxml2-devel zlib zlib-devel file-devel postgresql postgresql-devel postgresql-contrib geoip geoip-devel graphviz graphviz-devel gettext libtiff-devel libjpeg-devel libzip-devel freetype-devel lcms2-devel libwebp-devel tcl-devel tk-devel

    wget http://download.osgeo.org/proj/proj-4.8.0.zip
    unzip proj-4.8.0.zip && cd proj-4.8.0
    ./configure && make && sudo make install
    cd ..

    wget http://download.osgeo.org/geos/geos-3.4.2.tar.bz2
    tar -xvf geos-3.4.2.tar.bz2 && cd geos-3.4.2
    ./configure && make && sudo make install
    cd ..

    wget http://download.osgeo.org/gdal/1.10.1/gdal1101.zip
    unzip gdal1101.zip && cd gdal-1.10.1
    ./configure --with-python=yes && make && sudo make install
    cd ..

    wget http://download.osgeo.org/postgis/source/postgis-2.1.1.tar.gz
    tar -xvf postgis-2.1.1.tar.gz && cd postgis-2.1.1
    ./configure && make && sudo make install

    sudo echo /usr/local/lib >> /etc/ld.so.conf
    sudo ldconfig

    add postgis extension to database
    http://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.PostgreSQL.CommonDBATasks.html#Appendix.PostgreSQL.CommonDBATasks.PostGIS
