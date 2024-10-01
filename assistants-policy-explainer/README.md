# OpenAI Assistants API with File Search capabilities
* https://github.com/szilvia-csernus/openai-assistants-with-file-search


# Policy Explainer

I uploaded 2 files programmatically to OpenAI's Vector Store, one in .pdf and one in .md format, both covering policy documents for a ficticious company. OpenAI takes care of creating chunks and embeddings in an optimised way, no need to address these ourselves. I'm using the Assistants API to search these files to answer user questions, using the uploaded files as embedded documents. The Assistant automatically decides which document to use and answers the related questions correctly:

![policy-answer.png](./images/policy-answer.png)


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
```

Setup `.env` file:
```sh
$ touch .env

# Once you add your API key below, make sure to not share it with anyone! The API key should remain private.
OPENAI_API_KEY=abc123
```

# Run and test 

Run directly
```sh
$ pipenv run python searcher.py
```

Activate then run
```sh
$ pipenv shell
$ pipenv install
$ python company-assistant.py
```

Here is the first starting application:
```sh
$ python company-assistant.py

Using OpenAI SDK version 1.50.2
Step 1: Createing a new Assistant with File Search Enabled
New assistant is created with id = asst_YKZmZCpk6f7v4GWIypo7bslE
Saved the Assistant ID = asst_YKZmZCpk6f7v4GWIypo7bslE
Step 2: Uploading files and add them to a Vector Store
New vector store is created with id = vs_NcutRN72fv71jVZRwTtVwPvx
Uploading files to Vector Store: vs_NcutRN72fv71jVZRwTtVwPvx
Added FileCounts(cancelled=0, completed=1, failed=0, in_progress=0, total=1) files to Vector Store: vs_NcutRN72fv71jVZRwTtVwPvx with status: completed
Saved the Vector Store ID = vs_NcutRN72fv71jVZRwTtVwPvx
Step 3: Updating the assistant to to use the new Vector Store
Saved the Assistant ID = asst_YKZmZCpk6f7v4GWIypo7bslE
Step 4: Creating a thread
New thread is created 
Thread(id='thread_stwLyWwyjsTCdVV1Mj7nTHX3', created_at=1727768853, metadata={}, object='thread', tool_resources=ToolResources(code_interpreter=None, file_search=None))
Saved the Thread ID = thread_stwLyWwyjsTCdVV1Mj7nTHX3
Step 4: Creating a run and check the output
Enter a question, or type 'exit' to end: 
```

Here is the first uploaded file `company-policy.md` conversation:
```bash
Enter a question, or type 'exit' to end: Can I bring my pet cat into the office?
assistant: Based on the company policy documents uploaded, there is no specific mention of bringing pets, including cats, into the office. The policy mainly focuses on areas like respect and professionalism, attendance, health and safety, environmental sustainability, operational procedures, employee development, conduct outside the workplace, disciplinary actions, and policy amendments. There isn't a direct rule regarding pets in the office in the provided policy documents【4:0†source】【4:1†source】. If you are considering bringing your cat to the office, you may want to consult with HR or a supervisor to inquire about any specific pet policies that may exist.
```

We continue updating PET Policies into the knowledge base of the Assistant:
```bash
Adding file uploads/health-and-safety-policy.pdf to Vector Store vs_NcutRN72fv71jVZRwTtVwPvx
Added FileCounts(cancelled=0, completed=1, failed=0, in_progress=0, total=1) files to Vector Store: vs_NcutRN72fv71jVZRwTtVwPvx with status: completed
Saved the Vector Store ID = vs_NcutRN72fv71jVZRwTtVwPvx
Saved the uploaded files of Vectore store: vs_NcutRN72fv71jVZRwTtVwPvx
```