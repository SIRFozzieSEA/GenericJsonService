# Notes
sudo apt-get update && sudo apt-get dist-upgrade
sudo apt-get install python3-pip apache2 libapache2-mod-wsgi-py3 libpq-dev sqlite

# Make Virtual Environment in Root of Project
sudo pip3 install virtualenv
virtualenv env
source env/bin/activate
pip3 install django
pip3 install djangorestframework
pip3 install django-cors-headers

nano GenericJsonService/settings.py
Add - ALLOWED_HOSTS = ["server_domain_or_IP"]
Add - STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py collectstatic
python3 manage.py runserver 0.0.0.0:8000
python3 manage.py runserver ec2-3-84-78-247.compute-1.amazonaws.com:8000
deactivate

# Apache2 Stuffs
cd /etc/apache2/sites-available/
sudo nano pythonapi.conf
sudo a2ensite pythonapi.conf

<VirtualHost *:80>

        DocumentRoot /home/ubuntu/GenericJsonService
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        Alias /static /home/ubuntu/GenericJsonService/static
        <Directory /home/ubuntu/GenericJsonService/static>
                Require all granted
        </Directory>

        <Directory /home/ubuntu/GenericJsonService>
                <Files wsgi.py>
                        Require all granted
                </Files>
        </Directory>

        WSGIDaemonProcess GenericJsonService python-path=/home/ubuntu/GenericJsonService python-home=/home/ubuntu/GenericJsonService/env
        WSGIProcessGroup GenericJsonService
        WSGIScriptAlias / /home/ubuntu/GenericJsonService/wsgi.py
</VirtualHost>

chmod 664 /home/ubuntu/GenericJsonService/db.sqlite3
sudo chown :www-data /home/ubuntu/GenericJsonService/db.sqlite3
sudo chown :www-data /home/ubuntu/GenericJsonService

sudo /etc/init.d/apache2 restart
sudo /etc/init.d/apache2 stop

# SQL Iterations
sudo apt install postgresql postgresql-contrib
sudo -i -u postgres
psql\q

CREATE ROLE postgres WITH LOGIN CREATEDB ENCRYPTED PASSWORD 'admin';
ALTER ROLE postgres WITH PASSWORD 'admin';

pg_dump -Fc --username postgres > C:\_SORT\other\backup.pgsql
sudo service postgresql restart
dropdb --host=localhost --username postgres postgres
sudo -u postgres psql
createdb postgres
pg_restore --host=localhost --username=postgres -C -d postgres backup.pgsql

create table grocery_list (user TEXT, item TEXT);
insert into grocery_list values ('stephan', '{"buyGroceryItems": [{ "itemName": "Bread" },{ "itemName": "Eggs" },{ "itemName": "Milk" }],"boughtGroceryItems":[{ "itemName": "Bacon" },{ "itemName": "Potatoes" }]}');

# Resources
https://medium.com/@miracleaayodele/deploy-django-on-apache-mod-wsgi-747c6e4db9d1
https://medium.com/saarthi-ai/ec2apachedjango-838e3f6014ab
https://tecadmin.net/install-django-on-ubuntu/
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04
https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-16-04
https://www.metaltoad.com/blog/hosting-django-sites-apache
https://www.simplifiedpython.net/python-django-tutorial-for-beginners/


