# Apple ChatBot

Assistants API V1 using `retrieval` tools

# Setup environment

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

Loading .env environment variables...
Creating a virtualenv for this project...
Pipfile: /home/tvt/techspace/openai/openai-best-practices/assistants-apple-chatbot/Pipfile
Using default python from /home/tvt/.pyenv/versions/3.10.14/bin/python3.10 (3.10.14) to create virtualenv...
⠙ Creating virtual environment...created virtual environment CPython3.10.14.final.0-64 in 539ms
  creator CPython3Posix(dest=/home/tvt/.local/share/virtualenvs/assistants-apple-chatbot-reukysUY, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/home/tvt/.local/share/virtualenv)
    added seed packages: pip==24.1.2, setuptools==70.2.0, wheel==0.43.0
  activators BashActivator,CShellActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator

✔ Successfully created virtual environment!
Virtualenv location: /home/tvt/.local/share/virtualenvs/assistants-apple-chatbot-reukysUY
requirements.txt found in /home/tvt/techspace/openai/openai-best-practices/assistants-apple-chatbot instead of Pipfile! Converting...
✔ Success!
Warning: Your Pipfile now contains pinned versions, if your requirements.txt did. 
We recommend updating your Pipfile to specify the "*" version, instead.
Launching subshell in virtual environment...
```

If you want to get out of the virtual environment:
```sh
$ deactivate
$ exit
```

Install dependencies
```sh
$ pipenv install -r requirements.txt
```

You can verify the exact OpenAI version
```sh
$ pip list | grep openai
openai            1.16.1
```

# Run application

You can run main.py directly:
```sh
$ pipenv run main.py
```

You can activate the virtual environment then run the file
```sh
$ pipenv shell
$ python main.py 

$ python main.py
$ python main.py
Using OpenAI SDK version 1.16.1
OpenAI version is compatible.
 * Serving Flask app 'main'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://172.29.248.234:8080
Press CTRL+C to quit
 * Restarting with stat
Using OpenAI SDK version 1.16.1
OpenAI version is compatible.
 * Debugger is active!
 * Debugger PIN: 598-929-310
```


# Management Operations

List all uploaded files
```sh
curl --location --request GET 'http://localhost:8080/manage/files'
```

Upload a new file
```sh
curl --location --request POST 'http://localhost:8080/manage/files' \
--header 'Content-Type: application/json' \
--data '{
    "filename": "smithsolar.docx"
}'
```

Retrieve file by ID:
```sh
curl --location --request GET 'http://localhost:8080/manage/files/file-LDj0pUaVKPfB6BhtaqeBUEQ6'
```

Delete file by ID:
```sh
curl --location --request DELETE 'http://localhost:8080/manage/files/file-YrwRUWJsFKb9ORCGzb1JFLdt'
```

List all assistants
```sh
curl --location --request GET 'http://localhost:8080/manage/assistants?order=desc&limit=20'
```

Create new assistant
```sh
curl --location --request POST 'http://localhost:8080/manage/assistants' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Apple Assistant Bot",
    "description": "The Apple chat assistant",    
    "instructions": "\n\nAct as an expert in understanding the content of a text. \nThe text is the content of the files attached to the assistant via file_ids and assistant_id.\n\nFirst, deeply understand the input question in content of thread.\n\nThen, answer the question based on the following criteria:\n\nYour response should adhere to the following criteria:\n- The answer must be extracted solely from the provided text.\n- Provide only the paragraph from which the answer is derived.\n- Break the answer into smaller parts if necessary.\n- The answer must be in Vietnamese.\n\nTry your best to find the answer, check the provided text carefully, paragraph by paragraph.\nIf you cannot find the answer, please provide an answer that is similar to the question.\nOr just say: \"Xin lỗi, tôi không trả lời được. Làm ơn đặt câu hỏi rõ ràng hơn.\"\n\nAll output must be in Vietnamese.\n\n",
    "file_ids": ["file-LDj0pUaVKPfB6BhtaqeBUEQ6"]
}'
```

Retrieve assistant by ID:
```sh
curl --location --request GET 'http://localhost:8080/manage/assistants/asst_O4pLEnb6vsjP5cnaVJY5WgE9'
```

Delete assistant:
```sh
curl --location --request DELETE 'http://localhost:8080/manage/assistants/asst_eSytwpf8LaGY0Nbl81FETJ3V'
```

Modify assistant:
```sh
curl --location --request PUT 'http://localhost:8080/manage/assistants/asst_eSytwpf8LaGY0Nbl81FETJ3V' \
--header 'Content-Type: application/json' \
--data '{
    "description": "The Apple chat assistant",
    "name": "Apple Bot",
    "file_ids": ["file-uJ8tZPc1f3KhglRdFcNWiFmB"],
    "instructions": "\n          The assistant, Apple Assistant, has been programmed to help supporter reps with learning ompany standard operating procedures.\n          A document has been provided with information on Apple processes and training info.\n          "
}'
```

Create new thread
```sh
curl --location --request POST 'http://localhost:8080/manage/threads'
```

Retrieve thread
```sh
curl --location --request GET 'http://localhost:8080/manage/threads/thread_LA73Li3BuSi2YriSiJI68SzN'
```

Delete thread
```sh
curl --location --request DELETE 'http://localhost:8080/manage/threads/thread_HQVrLdgFxO6s6LDnWPPp98B6'
```

Chat conversation
```sh
curl --location 'http://localhost:8080/chat' \
--header 'Content-Type: application/json' \
--data '{
    "assistant_id": "asst_9VHRcc85jszNubXXsr11WeZZ",
    "thread_id":"thread_LA73Li3BuSi2YriSiJI68SzN",
    "message": "Jony Ive rời Apple vào tháng nào năm nào?"
}'
```