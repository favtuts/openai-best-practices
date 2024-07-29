#  Python example app from the OpenAI API quickstart tutorial
* https://platform.openai.com/docs/quickstart

# Account setup

* First, create an [OpenAI account](https://platform.openai.com/signup) or [sign in](https://platform.openai.com/login)
* Next, Next, navigate to the [API key page](https://platform.openai.com/account/api-keys) and "Create new secret key"

# Step 1: Setting up Python

## Install Python

To download Python, head to the [official Python website](https://www.python.org/downloads/) and download the latest version. To use the OpenAI Python library, you need at least Python 3.7.1 or newer. If you are installing Python for the first time, you can follow the [official Python installation guide for beginners](https://wiki.python.org/moin/BeginnersGuide/Download).

## Set up a virtual environment (optional)

It is a good practice to create a [virtual python environment](https://docs.python.org/3/tutorial/venv.html) to install the OpenAI Python library. Virtual environments provide a clean working space for your Python packages to be installed so that you do not have conflicts with other libraries you install for other projects.

Running the command below will create a virtual environment named "openai-env" inside the current folder you have selected in your terminal / command line:
```sh
$ cd openai-quickstart-python
$ python -m venv venv
```

Once you’ve created the virtual environment, you need to activate it.
```sh
$ source venv/bin/activate
```

## Install the OpenAI Python library

The OpenAI Python library can be installed. From the terminal / command line, run:
```sh
$ pip install --upgrade openai
```

Once this completes, running `pip list` will show you the Python libraries you have installed in your current environment
```sh
$ pip list
Package           Version
----------------- --------
annotated-types   0.7.0
anyio             4.4.0
certifi           2024.7.4
distro            1.9.0
exceptiongroup    1.2.2
h11               0.14.0
httpcore          1.0.5
httpx             0.27.0
idna              3.7
openai            1.37.1
pip               24.1.2
pydantic          2.8.2
pydantic_core     2.20.1
setuptools        65.5.0
sniffio           1.3.1
tqdm              4.66.4
typing_extensions 4.12.2
```

# Step 2: Set up your API key

## Set up your API key for all projects (recommended)

The main advantage to making your API key accessible for all projects is that the Python library will automatically detect it and use it without having to write any code.

Edit Bash Profile: Use the command `nano ~/.bash_profile` or `nano ~/.zshrc` (for newer MacOS versions) to open the profile file in a text editor.

Add Environment Variable: In the editor, add the line below, replacing your-api-key-here with your actual API key:
```sh
export OPENAI_API_KEY='your-api-key-here'
```

Load Your Profile: Use the command `source ~/.bash_profile` or `source ~/.zshrc` to load the updated profile.

Verification: Verify the setup by typing `echo $OPENAI_API_KEY` in the terminal. It should display your API key.


## Set up your API key for a single project

If you only want your API key to be accessible to a single project, you can create a local `.env` file which contains the API key and then explicitly use that API key with the Python code shown in the steps to come.

Start by going to the project folder you want to create the `.env` file in.

The `.env` file should look like the following:
```ini
# Once you add your API key below, make sure to not share it with anyone! The API key should remain private.

OPENAI_API_KEY=abc123
```

The API key can be imported by running the code below:
```python
from openai import OpenAI

client = OpenAI()
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
# client = OpenAI(
#   api_key=os.environ.get("CUSTOM_ENV_NAME"),
# )
```

# Step 3: Sending your first API request

## Making an API request

After you have Python configured and set up an API key, the final step is to send a request to the OpenAI API using the Python library. To do this, create a file named openai-test.py using th terminal or an IDE.

Inside the file, copy and paste one of the examples below:

```python
from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)
```

We need to use [Python Dotenv Library](https://pypi.org/project/python-dotenv). Just install the library `pip install python-dotenv`, create a `.env` file with your environment variables. 

To run the code, enter `python openai-test.py` into the terminal / command line.
```sh
$ $ python openai-test.py 
PROJECT_NAME: openai_quickstart_python
ChatCompletionMessage(content='In the land of code, where functions dwell,\nThere lies a magical process to tell.\nRecursion, the word whispered with grace,\nA concept woven throughout time and space.\n\nA function calling itself, daring and brave,\nSolving problems in a recursive wave.\nLike a mirror reflecting its own reflection,\nRecursion dives deep, creating connection.\n\nThrough loops and calls, it travels afar,\nUnraveling mysteries, like a shining star.\nEach iteration a step, a loop in time,\nUnfolding the code like a rhythmic chime.\n\nA journey through layers, nested and deep,\nA recursive dance, a rhythm to keep.\nBreaking down tasks into smaller parts,\nRecursion unfolds, connecting hearts.\n\nSo next time you code, with problems complex,\nRemember recursion, a powerful text.\nA looping saga, a story untold,\nIn the realm of programming, a treasure to behold.', role='assistant', function_call=None, tool_calls=None)
```
