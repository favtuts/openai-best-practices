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

Setup `.env` file:
```sh
$ touch .env

# Once you add your API key below, make sure to not share it with anyone! The API key should remain private.
OPENAI_API_KEY=abc123
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
The application will then be available at `localhost:5000`. You can test the functionality manually using `curl`, e.g. via
```sh
curl localhost:5000/api/v1/systeminfo/healthcheck
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
# kill -9 $(lsof -i :5000)
lsof -t -i:5000 | xargs kill -9
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

Now the application is served on `localhost:8600`. To run the automated tests for the production host, use
```sh
pytest --host http://localhost:8600
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
# kill -9 $(lsof -i :8600)
lsof -t -i:8600 | xargs kill -9
```

To stop the app in Production environment, execute
```sh
./bin/stop_app_prod.sh
```


# Test Endpoints

SystemInfo - HealthCheck:
```sh
curl --location 'http://localhost:5000/api/v1/systeminfo/healthcheck'
```

SystemInfo - VersionCheck:
```sh
curl --location 'http://localhost:5000/api/v1/systeminfo/versioncheck'
```

Assistant - Ask ChatGPT L1:
```sh
curl --location 'http://localhost:5000/api/v1/assistant/ask' \
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
curl --location 'http://localhost:5000/api/v1/assistant/askl22' \
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
curl --location 'http://localhost:5000/api/v1/assistant/createassistant' \
--header 'Content-Type: application/json' \
--data '{    
    "api_key": "sk-******"
}'
```

Assistant - Create new thread:
```sh
curl --location 'http://localhost:5000/api/v1/assistant/createthread' \
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

To view the API documentation through the Swagger user interface, navivate your browser to `http://localhost:5000/api/docs`.

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
$ pipenv run pytest --host http://localhost:8600
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

# Refernces
* [Minimal Flask Application for RESTful APIs](https://github.com/matdoering/minimal-flask-example)
* [A REST API template project developed with Python Flask](https://github.com/damianoalves/Flask-API)
* [A Clean Architecture Practice with Flask REST API](https://github.com/chonhan/flask_restapi_clean_architecture)
* [Production-ready REST API in Flask](https://github.com/ajoyoommen/flask-rest-api-template)