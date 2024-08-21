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