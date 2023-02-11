** For requirements.txt files 
pipreqs /path/to/project


[01:25, 18.04.2022] Said Taşdemir: 5 cihazı proxy için kullanabilme sorgu emri örneği:
# inmans django

Influencer Man Django Backhand 

## Başlamadan önce aşağıdaki satırı komut satırında çalıştırın:




# Server i çalıştırmak için komut satırında:

daphne -b 0.0.0.0 -p 8000 inmansdj.asgi:application -v2

export DJANGO_SETTINGS_MODULE=inmansdj.settings
heroku için: heroku config:set DJANGO_SETTINGS_MODULE=inmansdj.settings)
/usr/local/lib/python3.7/dist-packages

ssh root@37.221.122.37

WcMeedPOT2
# site configurations: for :80 port (without extra port)
sudo nano  /etc/apache2/sites-available/inmans.net.conf
sudo apache2ctl configtest

### All Cat files 
cat /etc/systemd/system/inmans.service
cat /etc/apache2/sites-available/inmans.net.conf
cat /usr/bin/inmans
# Re-start
sudo systemctl restart apache2
sudo systemctl restart inmans.service





######
root@ubuntu:~# cat /etc/systemd/system/inmans.service
[Unit]
Description=Inmans App.
After=weston.target

[Service]
Environment=DISPLAY=:0
PAMName=login
Type=simple
User=root
WorkingDirectory=/var/www/inmansdj/
ExecStart=bash /usr/bin/inmans
#ExecStart=/var/www/inmansdj/inmansdjenv/bin/daphne -b 0.0.0.0 -p 8001 inmansdj.asgi:application
Restart=always

[Install]
WantedBy=multi-user.target
root@ubuntu:~# cat /etc/apache2/sites-available/inmans.net.conf
<VirtualHost *:80>
    ServerAdmin webmaster@instatogether.com
    ServerName instatogether.com
    ServerAlias http://instatogether.com
    #DocumentRoot /var/www/inmansdj

    #WSGIDaemonProcess inmansdj python-path=/var/www/inmansdj python-home=/var/www/inmansdj/inmansenv
    #WSGIProcessGroup inmansdj
    #WSGIScriptAlias / /var/www/inmansdj/inmansdj/wsgi.py

    #Alias /robots.txt /var/www/inmansdj/static/robots.txt
    Alias /favicon.ico /var/www/inmansdj/static/favicon.ico

    Alias /media/ /var/www/inmansdj/media/
    Alias /static/ /var/www/inmansdj/static/

    <Directory /var/www/inmansdj/static>
        Require all granted
    </Directory>

    <Directory /var/www/inmansdj/media>
        Require all granted
    </Directory>

    # WSGIScriptAlias / /var/www/inmansdj/inmansdj/wsgi.py

    <Directory /var/www/inmansdj/inmansdj>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined

    <Location />
       ProxyPass http://localhost:8001/
       ProxyPassReverse http://localhost:8001/
    </Location>

#RewriteEngine on
#RewriteCond %{SERVER_NAME} =instatogether.com [OR]
#RewriteCond %{SERVER_NAME} =http://instatogether.com
#RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
</VirtualHost>

root@ubuntu:~# cat /usr/bin/inmans
#!/bin/bash
# cd /var/www/inmansdj
#echo '/var/www/inmansdj'
source /var/www/inmansdj/inmansdjenv/bin/activate
#echo '/var/www/inmansdj/inmansdjenv/bin/activate'
export DJANGO_SETTINGS_MODULE=inmansdj.settings
#echo 'daphne -b 0.0.0.0 -p 8001 inmansdj.asgi:application'
daphne -b 0.0.0.0 -p 8001 inmansdj.asgi:application -v2

root@ubuntu:~# cat /usr/bin/start
#!/bin/bash
cd /var/www/inmansdj
#echo '/var/www/inmansdj'
source /var/www/inmansdj/inmansdjenv/bin/activate
#echo '/var/www/inmansdj/inmansdjenv/bin/activate'
export DJANGO_SETTINGS_MODULE=inmansdj.settings
git pull
sudo systemctl restart inmans.services