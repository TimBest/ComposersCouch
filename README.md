Django powered site for composers couch

  Setting development to true
    add 'DEVELOPMENT=True' to the end of ~/.bashrc
    add 'export DEVELOPMENT=Treu' to the end of ~/.profile
    load with source ~/.bashrs and ~/.profile respectivly

  SSH into production server
    ssh -i djangosite-eb.pem ec2-user@54.174.202.254
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

  Load Location Data
    python manage.py shell
      from contact import load
      load.run()

  Load Genre Data
    python manage.py shell
      from genres import load
      load.run()
