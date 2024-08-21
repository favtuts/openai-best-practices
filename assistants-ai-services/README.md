# Create Real Production AI Services using Flask and OpenAI

# Prepare environment
Ensure to use Python3.10
```sh
$ python3 --version
Python 3.10.14
```

Install the Pipenv:
```sh
$ pip install --upgrade pip
$ pip install pipenv
```

Activate the virtual environment
```sh
$ pipenv shell
```

Get out of the virtual environment
```sh
$ deactivate
$ exit
```

Install dependencies
```sh
$ pipenv install openai
$ pipenv install python-dotenv[cli]
$ pipenv install packaging
$ pipenv install uwsgi
$ pipenv install werkzeug
$ pipenv install pytest
$ pipenv install requests
```

For deployment, we need install all libraries in `Pipfile`
```sh
$ pipenv install
```

# Development Environment

Create executable file for starting up Application on Development environment
```sh
# create the file
touch bin/run_app_dev.sh

# make it executable
chmod +x bin/run_app_dev.sh
```

Input the content to the file
```sh
#!/bin/bash
FLASK_ENV=development pipenv run flask run

```

To start the app in development mode, execute
```sh
./bin/run_app_dev.sh
```
The application will then be available at `localhost:5432`. You can test the functionality manually using `curl`, e.g. via
```sh
curl localhost:5432/api/v2/systeminfo/healthcheck
```
or through the automated tests, by running
```sh
pytest
```

Create the executable file for shutting down the Development environment:
```sh
# create the file
touch bin/stop_app_dev.sh

# make it executable
chmod +x bin/stop_app_dev.sh
```

Input the content to the file
```sh
#!/bin/bash
# https://stackoverflow.com/questions/33615683/how-to-access-the-pid-from-an-lsof
# kill -9 $(lsof -i :5432)
lsof -t -i:5432 | xargs kill -9
```

To stop the app in Development environment, execute
```sh
./bin/stop_app_dev.sh
```


# Production Environment

Create executable file for starting up Application on Production environment
```sh
# create the file
touch bin/run_app_prod.sh

# make it executable
chmod +x bin/run_app_prod.sh
```

Input the content to the file
```sh
#!/bin/bash
pipenv uwsgi --ini app.ini --need-app

```

To run the app in production, execute
```sh
./bin/run_app_prod.sh
```

Now the application is served on `localhost:8432`. To run the automated tests for the production host, use
```sh
pytest --host http://localhost:8432
```

Create the executable file for shutting down the Production environment:
```sh
# create the file
touch bin/stop_app_prod.sh

# make it executable
chmod +x bin/stop_app_prod.sh
```

Input the content to the file
```sh
#!/bin/bash
# https://stackoverflow.com/questions/33615683/how-to-access-the-pid-from-an-lsof
# kill -9 $(lsof -i :8432)
lsof -t -i:8432 | xargs kill -9
```

To stop the app in Production environment, execute
```sh
./bin/stop_app_prod.sh
```


# Test Endpoints

SystemInfo - HealthCheck:
```sh
curl --location 'http://localhost:5432/api/v2/systeminfo/healthcheck'
```

SystemInfo - VersionCheck:
```sh
curl --location 'http://localhost:5432/api/v2/systeminfo/versioncheck'
```

Assistant - Ask ChatGPT L1:
```sh
curl --location 'http://localhost:5432/api/v2/assistant/ask' \
--header 'Content-Type: application/json' \
--data '{
    "question": "vietin bank la ngan hang nao",
    "assistant_id": "asst_zTZ7YRpYOQbUREMucnCc9kC6",
    "thread_id": "thread_u003zMFEOYmCT4dAO8CcnRjI",
    "api_key": "sk-******"
}'
```

Assistant - Ask ChatGPT L12:
```sh
curl --location 'http://localhost:5432/api/v2/assistant/askl22' \
--header 'Content-Type: application/json' \
--data '{
    "question": "vietin bank la ngan hang nao",
    "assistant_id": "asst_zTZ7YRpYOQbUREMucnCc9kC6",
    "thread_id": "thread_u003zMFEOYmCT4dAO8CcnRjI",
    "api_key": "sk-******"
}'
```

Assistant - Create new assistant:
```sh
curl --location 'http://localhost:5432/api/v2/assistant/createassistant' \
--header 'Content-Type: application/json' \
--data '{    
    "api_key": "sk-******"
}'
```

Assistant - Create new thread:
```sh
curl --location 'http://localhost:5432/api/v2/assistant/createthread' \
--header 'Content-Type: application/json' \
--data '{    
    "api_key": "sk-******"
}'
```


# Swagger Documentation

Install dependencies to support Swagger API Docs
```sh
# swagger api docs
pipenv install apispec
pipenv install apispec_webframeworks
pipenv install marshmallow
pipenv install flask_swagger_ui
pipenv install openapi_spec_validator
```

To view the API documentation through the Swagger user interface, navivate your browser to `http://localhost:5432/api/docs`.

# Endpoint Unit Testing

Install the `pytest` library
```sh
$ pipenv install pytest
$ pipenv install requests
```

To run testing on Development
```sh
$ pipenv run pytest
```

To run testing on Production
```sh
$ pipenv run pytest --host http://localhost:8432
```

# Configureation 

Auto detect the environment via `FLASK_ENV` variable, then dynamic loading config based on corresponding file.

Install the `python-dotenv` library:
```sh
$ pipenv install python-dotenv[cli]
```


# Count tokens with Tiktoken
* https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken

Install `tiktoken`
```sh
$ pipenv install tiktoken
```

If you need to install the latest version
```sh
$ pipenv update tiktoken 
```

# System Prodoction Deployment
* https://www.shubhamdipt.com/blog/how-to-create-a-systemd-service-in-linux/
* https://unix.stackexchange.com/questions/225401/how-to-see-full-log-from-systemctl-status-service
* https://www.linode.com/docs/guides/how-to-use-journalctl
* https://www.baeldung.com/linux/redirect-systemd-output-to-file

Checking Python3 environment
```sh
$ conda deactivate
$ python3 --version
Python 3.10.12
$ pip --version
pip 22.0.2 from /usr/lib/python3/dist-packages/pip (python 3.10)
$ pip install --upgrade pip
Defaulting to user installation because normal site-packages is not writeable
Requirement already satisfied: pip in /usr/lib/python3/dist-packages (22.0.2)
Collecting pip
  Downloading pip-24.2-py3-none-any.whl (1.8 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 736.2 kB/s eta 0:00:00
Installing collected packages: pip
Successfully installed pip-24.2
$ pip install pipenv
$ pipenv --version
$ pip install --user pipenv
```

Copy code to folder `/emteller/assistant_api` using WinSCP
```sh
$ cd /emteller/assistant-api/
```
Install all dependencies in Pipfile.lock
```sh
$ pipenv install
$ pipenv graph
$ pipenv --where
$ pipenv --venv
/home/nsd/.local/share/virtualenvs/assistant-api-7J-tQlj6
```

Can activate the environment
```sh
$ pipenv shell
Launching subshell in virtual environment...
 . /home/nsd/.local/share/virtualenvs/assistant-api-7J-tQlj6/bin/activate
(base) nsd@nsd-OBS:/emteller/assistant-api$  . /home/nsd/.local/share/virtualenvs/assistant-api-7J-tQlj6/bin/activate
```

Allow executable scripts
```sh

$ chmod +x bin/run_app_prod.sh
$ chmod +x bin/run_app_dev.sh
$ chmod +x bin/stop_app_prod.sh
$ chmod +x bin/stop_app_dev.sh
```

Check all emteller services
```sh
sudo systemctl list-units | grep emteller
```

Create new service file:
```sh
$ sudo nano /etc/systemd/system/emteller-api.service

[Unit]
Description=EMTELLER ASSISTANT APIs

[Service]
User=nsd
WorkingDirectory=/emteller/assistant-api
ExecStart=/bin/bash /emteller/assistant-api/bin/run_app_prod.sh
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Reload the service files to include the new service.
```sh
sudo systemctl daemon-reload
systemctl --now enable emteller-api.service
```

Start your service
```sh
sudo systemctl start emteller-api.service
```

To check the status of your service
```sh
sudo systemctl status emteller-api.service
journalctl -xeu emteller-api.service
```

To enable your service on every reboot
```sh
sudo systemctl enable emteller-api.service
```

ExecStart=/emteller/assistant-api/bin/run_app_prod.sh
/emteller/assistant-api/bin/run_app_prod.sh

To disable your service on every reboot
```sh
sudo systemctl disable emteller-api.service
```

To view log
```sh
sudo journalctl -u emteller-api.service -b -f

# the -e option at end jumps to end of the logfile to see most recent logs.
sudo journalctl -u emteller-api.service -e
```

View `journalctl` without Paging
```sh
sudo journalctl -u emteller-api.service --no-pager
```

Show Logs within a Time Range
```sh
journalctl --since "2018-08-30 14:10:10"
journalctl --until "2018-09-02 12:05:50"
journalctl --since "2018-08-30 14:10:10" --until "2018-09-02 12:05:50"
```

Most of the time, it is convenient and easy to use the following bash command:
```sh
journalctl -xefu emteller-api.service
```

Using journalctl, write logs to a text file, and read it bottom up:
```sh
journalctl -u emteller-api.service > file_name.txt &&\
tail file_name.txt
```

# Allow port for remote access
* https://www.cyberciti.biz/faq/how-to-open-firewall-port-on-ubuntu-linux-12-04-14-04-lts/

Normal it is starting on port 8432:
```sh
 uwsgi socket 0 bound to TCP address 127.0.0.1:8432
```

To see the current status of my firewall
```sh
sudo ufw status verbose
sudo ufw status verbose | grep 8432
```

How do I open tcp port # 8432
```sh
$ sudo ufw allow 8432/tcp
Rule added
Rule added (v6)

$ sudo ufw status verbose
```

Check Ubuntu IP
```sh
$ hostname -I
192.168.0.131 172.17.0.1 172.19.0.1
```

Change the `app.ini` the IP Address
```ini
[uwsgi]
http-socket = 0.0.0.0:8432
```

Now you can telnet from remote:
```sh
$ telnet 192.168.0.131 8432
```


# Refernces
* [Minimal Flask Application for RESTful APIs](https://github.com/matdoering/minimal-flask-example)
* [A REST API template project developed with Python Flask](https://github.com/damianoalves/Flask-API)
* [A Clean Architecture Practice with Flask REST API](https://github.com/chonhan/flask_restapi_clean_architecture)
* [Production-ready REST API in Flask](https://github.com/ajoyoommen/flask-rest-api-template)