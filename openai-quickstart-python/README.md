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