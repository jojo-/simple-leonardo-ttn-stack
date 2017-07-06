# Installation of the dashboard

You need a Python 3 environment with the following modules installed:
- Flask;
- uWSGI;
- sqlite3;
- datetime;
- and json.

Note that the dashboard is also compatible with a Python 2 environment.

Before using the dashboard
- the path to the databases should be set in the file `sensors.py`
- and you need to provide a key to use the Google Map api in the htlm files located in the `template` directory.

Once this is done, the dashboard can be tested by typing:

`python3 sensors.py`

and then opening a web browser and navigate to either
- <http://0.0.0.0:8080/track_data>;
- or <http://0.0.0.0:8080/track_htpp>.

To update the database obtained from the TTN Data Integration (<https://binarybeer.data.thethingsnetwork.org/>), you must run the script `update_db.py`. Please make sure that the path to the data base is correct, and that the authorization is set in the `headers` variable. For more convenience, you can add that script to a Cron job.

# Deploying the dashboard in a Debian environment

## Dashboard

Set the Flask debugging flag `app.debug` to `False` in the file `sensors.py`.

## Installation of NGINX

1. In the directory /etc/nginx/sites-enabled/, create a symbolic link to the sensors_nginx.conf.
2. Remove the file default.conf in the /etc/nginx/sites-enabled directory.
3. Make sure that the service starts at boot: `sudo systemctl enable nginx`.

## Installation of uWSGI:

1. Copy uwsgi.service file in /lib/systemd/system/.
2. In the directory /etc/uwsgi/vassals/, create a symbolic link to the sensors_uwsgi.ini.
3. Make sure that the service starts at boot: `sudo systemctl enable uwsgi`.

**Note:** 

Please make sure that the permissions are set to allow uWSGI and NGINX to read/write the logs, data and socket files.




