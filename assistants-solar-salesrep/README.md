# How to Create Your Own GPT with OpenAI’s Assistants API
* https://tuts.heomi.net/how-to-create-your-own-gpt-with-openais-assistants-api/
* https://youtu.be/Uk5f3ajkfSs?si=2EEW4wLPNlZPE27n

# Setup Python virtual environment

Using Python3.10
```sh
$ python3 --version
Python 3.10.14
```

Create a new virtual environment
```sh
$ python -m venv venv
$ . venv/bin/activate
or 
$ source venv/bin/activate
```
Install the OpenAI Python library
```sh
$ pip install --upgrade pip
$ pip install --upgrade openai
```
Run `pip list` command to check
```sh
$ pip list | grep "openai"

openai            1.37.1
```

Setup .env file:
```sh
$ touch .env
```

Using [python-dotenv](https://pypi.org/project/python-dotenv) library to load environment variables.
```sh
$ pip install python-dotenv[cli]
```

OPENAI_API_KEY=abc123

Add the OPENAI_API_KEY variable
```sh
$ dotenv set OPENAI_API_KEY abc123
$ dotenv list
OPENAI_API_KEY=abc123
```

# Changing beta versions

## Without SDKs**

Both beta versions can be accessed by passing the right API version header in your API requests:

* v1: `OpenAI-Beta: assistants=v1`
* v2: `OpenAI-Beta: assistants=v2`

```python
curl "https://api.openai.com/v1/assistants" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "OpenAI-Beta: assistants=v2" \
  -d '{
    "instructions": "You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
    "name": "Math Tutor",
    "tools": [{"type": "code_interpreter"}],
    "model": "gpt-4-turbo"
  }'
```

## With SDKs

Versions of our SDKs that are released after the release of the `v2` beta will have the `openai.beta` namespace point to the `v2` version of the API by default. You can still access the `v1` version of the API by using an older version of the SDK (1.20.0 or earlier for python, 4.36.0 or earlier for node) or by overriding the version header.

To install an older version of the SDK, you can use the following commands:
Installing older versions of the SDK
```sh
pip install openai==1.20.0
```

You can also override this header in a newer SDK version, but we don't recommend this approach since the object types in these newer SDK versions will be different from the `v1` objects.
Accessing the `v1` API version in new SDKs
```python
from openai import OpenAI

client = OpenAI(default_headers={"OpenAI-Beta": "assistants=v1"})
```


## Requirement.txt

```sh
pip3 freeze > requirements.txt
```

# Create assistant

Create file [functions.py](functions.py) is used to create new assistant and saved it to `assistant.json` by following steps:
1. Uploads a single knowledge base file `knowledge.docx`
```python
file = client.files.create(file=open("knowledge.docx", "rb"),
                               purpose='assistants')
```

2. Create assistant object by providing parameters `instructions`, `model`, `tools`, and `file_ids` according to your specific use case and your needs.
Example:
```python
# client.beta.assistants.create() returns an assistant object
my_assistant = client.beta.assistants.create(
  instructions="You help users create recipes for meals that are healthy, inexpensive, and quick to prepare. You should respond to the user’s wishes, cooking preferences and tastes and provide suitable dishes with the corresponding recipes. Users may have different prior knowledge about the respective dishes. Some users may not have cooked very often before.",
  name="Recipe Wizard",
  tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
  file_ids=[my_file.id],
  model="gpt-4"
)
```

# Create API endpoints

Create file [main.py](main.py) which initializes the `client`, calls the function `create_assistant(client)` of [functions.py](./functions.py). Next, it defines two routes /endpoints of the Flask app:
* `/start`: This route starts a new conversation thread. When accessed via a GET request, it creates a new thread using OpenAI's API and returns the thread ID in JSON format
* `/chat`: This route handles incoming POST requests containing JSON data with a `thread_id` and a `message`. It adds the user's message to the specified `thread`, runs the assistant to generate a response, and returns the response in JSON format.

Install the [`packaging` library](https://packaging.pypa.io/en/stable/) for version checking:
```sh
$ pip install packaging
```

Install the `Flask library`(https://flask.palletsprojects.com/en/3.0.x/installation/) for API endpoints
```sh
$ pip install Flask
```


# Run and Test the Assistant

```sh
$ source venv/bin/activate
$ python main.py 

Using OpenAI SDK version 1.20.0
OpenAI version is compatible.
Loaded existing assistant ID = asst_IKFsebHEgmnIcdpBTljNDxEu
Loaded existing thread ID = thread_KsQpEHWCLVE1PDjSjWhOweQE
 * Serving Flask app 'main'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://172.29.248.234:8080
Press CTRL+C to quit
```

Start chat
```sh
curl --location 'http://localhost:8080/chat' \
--header 'Content-Type: application/json' \
--data '{
    "thread_id":"thread_KsQpEHWCLVE1PDjSjWhOweQE",
    "message": "What discount do we have available?"
}'

{
    "response": "The available discounts at Smith Solar include:\n\n1. **Early Bird Discount**:\n   - A 15% discount on the total cost of any solar energy system for customers who sign contracts within the first week of their inquiry. This can result in significant savings for customers who act promptly【5†source】.\n\n2. **Referral Discounts**:\n   - Existing customers receive a $500 discount on their next purchase or a $500 cash rebate if they don't plan to make further purchases when they refer a new customer to Smith Solar who purchases a solar energy system. The newly referred customer also receives a $500 discount on their solar system.\n   - There is a special offer where if an existing customer refers three new customers within a year, they can get a free solar battery worth $3000【5†source】. \n\nThese discounts are designed to make solar energy more accessible and affordable to customers."
}
```

In the terminal
```sh
Received message: What discount do we have available? for thread ID: thread_KsQpEHWCLVE1PDjSjWhOweQE
Run status: in_progress
Run status: in_progress
Run status: in_progress
Run status: in_progress
Run status: completed
Assistant response: The available discounts at Smith Solar include:

1. **Early Bird Discount**:
   - A 15% discount on the total cost of any solar energy system for customers who sign contracts within the first week of their inquiry. This can result in significant savings for customers who act promptly【5†source】.

2. **Referral Discounts**:
   - Existing customers receive a $500 discount on their next purchase or a $500 cash rebate if they don't plan to make further purchases when they refer a new customer to Smith Solar who purchases a solar energy system. The newly referred customer also receives a $500 discount on their solar system.
   - There is a special offer where if an existing customer refers three new customers within a year, they can get a free solar battery worth $3000【5†source】. 

These discounts are designed to make solar energy more accessible and affordable to customers.
127.0.0.1 - - [31/Jul/2024 22:27:55] "POST /chat HTTP/1.1" 200 -
```

