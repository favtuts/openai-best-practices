#  Python example app from the OpenAI API quickstart tutorial
* https://platform.openai.com/docs/quickstart

# Account setup

* First, create an [OpenAI account](https://platform.openai.com/signup) or [sign in](https://platform.openai.com/login)
* Next, Next, navigate to the [API key page](https://platform.openai.com/account/api-keys) and "Create new secret key"

# Step 1: Setting up Python

## Install Python

To download Python, head to the [official Python website](https://www.python.org/downloads/) and download the latest version. To use the OpenAI Python library, you need at least Python 3.7.1 or newer. If you are installing Python for the first time, you can follow the [official Python installation guide for beginners](https://wiki.python.org/moin/BeginnersGuide/Download).

# Set up a virtual environment (optional)

It is a good practice to create a [virtual python environment](https://docs.python.org/3/tutorial/venv.html) to install the OpenAI Python library. Virtual environments provide a clean working space for your Python packages to be installed so that you do not have conflicts with other libraries you install for other projects.

Running the command below will create a virtual environment named "openai-env" inside the current folder you have selected in your terminal / command line:
```sh
$ cd openai-quickstart-python
$ python -m venv venv
```

Once you’ve created the virtual environment, you need to activate it.
```sh
source venv/bin/activate
```