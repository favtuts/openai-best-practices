# RabbitMQ Application workers


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
$ pipenv install playwright
$ pipenv install pika
$ pipenv install requests
```


# QA-Robot

Dependencies
```sh
google-generativeai
streamlit
pillow
pdf2image
pandas
openpyxl
pytesseract 
PyMuPDF
python-docx
langdetect
langcodes
language_data
thefuzz
openpyxl
tqdm
openai
unidecode
underthesea
```

# Start the Worker

Run directly
```sh
pipenv run l2_app.py
```

Or activate environment
```sh
pipenv shell
python l2_app.py
```

# Create shell script
* https://stackoverflow.com/questions/40652793/how-to-kill-python-script-with-bash-script
* https://stackoverflow.com/questions/17686351/shell-start-stop-for-python-script
* https://gist.github.com/justinemter/a8c71d0d21940fb69731c85159a01957

# Production Deployment

Copy code to folder
```sh
$ conda deactivate
cd /emteller/assistant-worker
```

Set file executables
```sh
$ chmod +x bin/run_app_prod.sh
$ chmod +x bin/stop_app_prod.sh
$ chmod +x bin/exec_app_prod.sh
```

Check python environment
```sh
$ python3 --version
$ pip --version
$ pip install pipenv
$ pip install --user pipenv
$ pipenv --version
```

Install all dependencies in Pipfile.lock
```sh
$ pipenv install
$ pipenv --venv
$ pipenv graph
```

Run test script
```sh
$ ./bin/run_app_prod.sh
$ ./bin/stop_app_prod.sh
```

Create new systemctl service file
```sh
$ sudo nano /etc/systemd/system/emteller-worker.service

[Unit]
Description=EMTELLER ASSISTANT WORKERs
After=syslog.target network.target
[Service]
User=nsd
Type=forking

WorkingDirectory=/emteller/assistant-worker
ExecStart=/usr/bin/bash /emteller/assistant-worker/bin/exec_app_prod.sh
ExecStop=/bin/kill -15 $MAINPID

SuccessExitStatus=143
Restart=on-failure

[Install]
WantedBy=multi-user.target
```


Reload the service files to include the new service.
```sh
sudo systemctl daemon-reload
systemctl --now enable emteller-worker.service
```

Start your service
```sh
sudo systemctl start emteller-worker.service
```

To stop your servie
```sh
sudo systemctl stop emteller-worker.service
```

To check the status of your service
```sh
sudo systemctl status emteller-worker.service
```

To enable your service on every reboot
```sh
sudo systemctl enable emteller-worker.service
```

To disable your service on every reboot
```sh
sudo systemctl disable emteller-worker.service
```

To view log
```sh
sudo journalctl -u emteller-worker.service -b -f

# the -e option at end jumps to end of the logfile to see most recent logs.
sudo journalctl -u emteller-worker.service -e
```

View `journalctl` without Paging
```sh
sudo journalctl -u emteller-worker.service --no-pager
```

Show Logs within a Time Range
```sh
journalctl --since "2018-08-30 14:10:10"
journalctl --until "2018-09-02 12:05:50"
journalctl --since "2018-08-30 14:10:10" --until "2018-09-02 12:05:50"
```

Most of the time, it is convenient and easy to use the following bash command:
```sh
journalctl -xefu emteller-worker.service
```

Using journalctl, write logs to a text file, and read it bottom up:
```sh
journalctl -u emteller-worker.service > file_name.txt &&\
tail file_name.txt
```

To check all emteller services running
```sh
sudo systemctl list-units | grep emteller
```