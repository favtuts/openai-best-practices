import os

from dotenv import load_dotenv
from dotenv import set_key
from pathlib import Path

from openai import OpenAI
from time import sleep

env_file_path = Path(".env")
# Create the file if it does not exist.
env_file_path.touch(mode=0o600, exist_ok=True)
load_dotenv(dotenv_path=env_file_path)

openai_apikey = ""
OPENAI_APIKEY = os.getenv('OPENAI_APIKEY')
if OPENAI_APIKEY is not None:
    openai_apikey = OPENAI_APIKEY

print("OPENAI_APIKEY: " +  openai_apikey)

starting_assistant = ""
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
if ASSISTANT_ID is not None:
    starting_assistant = ASSISTANT_ID

print("ASSISTANT_ID: " +  starting_assistant)

starting_thread = ""
THREAD_ID = os.getenv("THREAD_ID")
if THREAD_ID is not None:
    starting_thread = THREAD_ID
    
print("ASSISTANT_ID: " +  starting_thread)

CST_DEFAULT_MODEL_NAME="gpt-3.5-turbo"
starting_model = CST_DEFAULT_MODEL_NAME
MODEL_NAME = os.getenv("MODEL_NAME")
if MODEL_NAME is not None:
    starting_model = MODEL_NAME

print("MODEL_NAME: " +  starting_model)


client = OpenAI(
    api_key=openai_apikey,
)

"""
An Assistant represents an entity that can be configured to respond to a user's messages 
"""
def create_assistant():
    if starting_assistant == "":
        my_assistant = client.beta.assistants.create(
            name="Math Tutor",
            instructions="You are a personal math tutor. Write and run code to answer math questions.",
            tools=[{"type": "code_interpreter"}],
            model=starting_model,
        )
        if my_assistant is not None:
            # save new assistant id to env for next time
            write_env("ASSISTANT_ID", my_assistant.id)        
            print(f"new assistant is created with id = {my_assistant.id}")
    else:
        my_assistant = client.beta.assistants.retrieve(starting_assistant)
    
    return my_assistant



"""
A Thread represents a conversation between a user and one or many Assistants.
You can create a Thread when a user (or your AI application) starts a conversation with your Assistant.
"""
def create_thread():
    if starting_thread == "":
        thread = client.beta.threads.create()
        if thread is not None:
            # save new thread id to env for next time
            write_env("THREAD_ID", thread.id)        
            print(f"new thread is created with id = {thread.id}")
    else:
        thread = client.beta.threads.retrieve(starting_thread)
        
    return thread


"""
Add a Message to the Thread: 
The contents of the messages your users or applications create are added as Message objects to the Thread. 
Messages can contain both text and files
"""
def send_message(thread_id, message):
    thread_message = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=message,
    )
    return thread_message


"""
Create a Run
Once all the user Messages have been added to the Thread, you can Run the Thread with any Assistant
Creating a Run uses the model and tools associated with the Assistant to generate a response
"""
def run_assistant(thread_id, assistant_id, instructions=None):
    if instructions is None:
        run = client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=assistant_id
        )
    else:    
        run = client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=assistant_id, instructions=instructions
        )
    
    return run


def get_newest_message(thread_id):
    thread_messages = client.beta.threads.messages.list(thread_id)
    return thread_messages.data[0]

def get_run_status(thread_id, run_id):
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    return run.status

def main():
    
    my_assistant = create_assistant()    
    my_thread = create_thread()

    while True:
        user_message = input("Enter your message: ")
        if user_message.lower() == "exit":
            break
        
        send_message(my_thread.id, user_message)
        run = run_assistant(my_thread.id, my_assistant.id)
        while run.status != "completed":
            run.status = get_run_status(my_thread.id, run.id)
            sleep(1)
            print("⏳", end="\r", flush=True)

        sleep(0.5)
        response = get_newest_message(my_thread.id)
        print("Response:", response.content[0].text.value)


def write_env(key, value):    
    # Save some values to the file.
    set_key(dotenv_path=env_file_path, key_to_set=key, value_to_set=value)    
    
def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

def show_all_envs():
    ev = dict(os.environ)
    pretty(ev)
    
def write_default_env():
    # write key value pairs
    write_env("ASSISTANT_ID", "asst_zTZ7YRpYOQbUREMucnCc9kC6")
    write_env("THREAD_ID", "thread_u003zMFEOYmCT4dAO8CcnRjI")
    write_env("MODEL_NAME", "gpt-3.5-turbo")
    # reload env dictionary
    load_dotenv(env_file_path)
    # show all envs
    show_all_envs()
    
if __name__=="__main__":
    # write_default_env()
    main()