import os
import json
import time

from packaging import version

from dotenv import load_dotenv
import openai
from openai import OpenAI

load_dotenv()

openai_apikey = ""
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if OPENAI_API_KEY is not None:
    openai_apikey = OPENAI_API_KEY
    
client = OpenAI(
    api_key=openai_apikey,
)

assistant_file = "saved/assistant.json"
vector_store_file = "saved/vector_store.json"
thread_file = "saved/thread.json"
files_file = "saved/files.json"

# starting_model = "gpt-4o"
starting_model = "gpt-3.5-turbo"

def write_dictionary(my_dict, filename):
    # Overwrite the whole content
    with open(filename, "w") as infile:
        json.dump(my_dict, infile, sort_keys=True, indent=4)    

def read_dictionary(filename):
    if not os.path.exists(filename):
        return None
    with open(filename) as outfile:
        dict_data = json.load(outfile)
    return dict_data


# Create the assistant
def create_assistant():
    starting_assistant_id = ""
    assistant_dict = read_dictionary(assistant_file)
    if assistant_dict is not None:        
        starting_assistant_id = assistant_dict["id"]
        print(f"Existing Assistant Id = {starting_assistant_id}")  # Debugging line
        
    if starting_assistant_id == "":
        # create new assistant with file search enabled
        my_assistant = client.beta.assistants.create(
            name="Policy Explainer",
            instructions="You answer questions about company rules based on your knowledge of the company policy files.",
            tools=[{"type": "file_search"}],        
            model=starting_model,
        )        
        print(f"New assistant is created with id = {my_assistant.id}")  # Debugging line
        
        # save new assistant id to file for loading in the next time
        write_dictionary(my_assistant.model_dump(), assistant_file)
        print(f"Saved the Assistant ID = {my_assistant.id}")  # Debugging line 
    else:
        # retrieve assistant if it has been already created
        my_assistant = client.beta.assistants.retrieve(starting_assistant_id)
    
    return my_assistant

# Create a vector store
def create_vector_store(file_paths):
    starting_vector_store_id = ""
    vector_store_dict = read_dictionary(vector_store_file)
    
    if vector_store_dict is not None:       
        starting_vector_store_id = vector_store_dict["id"]
        print(f"Existing Vector Store Id = {starting_vector_store_id}")  # Debugging line
            
    if starting_vector_store_id == "":
        # Create a vector store caled "Company Policies"
        my_vector_store = client.beta.vector_stores.create(name="Company Policies")
        print(f"New vector store is created with id = {my_vector_store.id}")  # Debugging line
        
        print(f"Uploading files to Vector Store: {my_vector_store.id}")  # Debugging line
        
        # Ready the files for upload to OpenAI
        # file_paths = ["upload/file1.pdf", "upload/file2.txt"]
        file_streams = [open(path, "rb") for path in file_paths]
        
        # Use the upload and poll SDK helper to upload the files, add them to the vector store,
        # and poll the status of the file batch for completion.
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=my_vector_store.id, files=file_streams
        )
        
        # You can print the status and the file counts of the batch to see the result of this operation.
        print(f"Added {file_batch.file_counts} files to Vector Store: {my_vector_store.id} with status: {file_batch.status}")  # Debugging line
                
        # Retrieve vector store again after uploading files
        my_vector_store = client.beta.vector_stores.retrieve(my_vector_store.id)
        
        # save new vector store file for loading in the next time
        write_dictionary(my_vector_store.model_dump(), vector_store_file)
        print(f"Saved the Vector Store ID = {my_vector_store.id}")  # Debugging line
    else:
        # retrieve vector store if it has been already created
        my_vector_store = client.beta.vector_stores.retrieve(starting_vector_store_id)
    
    return my_vector_store


# Save uploaded files on specific vector store
def save_uploaded_files(vector_store_id):
    # retrieve file list of vector store
    my_vs_files = client.beta.vector_stores.files.list(vector_store_id)
    
    # save to files
    if my_vs_files != None:
        write_dictionary(my_vs_files.model_dump(), files_file)


# Add a new file to the vector store. Note, you don't need to update the assistant again
# as it's referring to the vector store id which has not changed.
def add_new_file_to_vector_store(vector_store_id, adding_file_path):
    adding_file_stream = open(adding_file_path, "rb")
    
    # Use the upload and poll SDK helper to upload the files, add them to the vector store,
    # and poll the status of the file batch for completion.
    adding_file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store_id, files=[adding_file_stream]
    )
    
    print(f"Added {adding_file_batch.file_counts} files to Vector Store: {vector_store_id} with status: {adding_file_batch.status}")  # Debugging line
    
    # Retrieve vector store again after uploading files
    adding_vector_store = client.beta.vector_stores.retrieve(vector_store_id)
    
    # save new vector store file for loading in the next time
    write_dictionary(adding_vector_store.model_dump(), vector_store_file)
    print(f"Saved the Vector Store ID = {adding_vector_store.id}")  # Debugging line
    
    # save uploaded files
    save_uploaded_files(vector_store_id)
    


def attach_vector_store_to_assistant(target_assistant, vector_store_id):            
    # Check if the assistant is already attached the Vector Store Id
    if vector_store_id in target_assistant.tool_resources.file_search.vector_store_ids:
        print(f"The target assistant already attach the Vector Store Id {vector_store_id}")  # Debugging line
        return target_assistant
    
    # To make the files accessible to your assistant, update the assistant’s tool_resources with the new vector_store id.
    attached_assistant = client.beta.assistants.update(
        assistant_id=target_assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
    )
    
    # save new assistant id to file for loading in the next time
    write_dictionary(attached_assistant.model_dump(), assistant_file)
    print(f"Saved the Assistant ID = {attached_assistant.id}")  # Debugging line
        
    return attached_assistant


def create_thread():
    starting_thead_id = ""
    thread_dict = read_dictionary(thread_file)
    if thread_dict is not None:
        starting_thead_id = thread_dict["id"]
        print(f"Existing Thread Id = {starting_thead_id}")  # Debugging line
        
    if starting_thead_id == "":
        
        # created_vector_store_dict = read_dictionary(vector_store_file)
        # created_vector_store_id = created_vector_store_dict["id"]
        
        # # create new thread
        # my_thread = client.beta.threads.create(
        #     tool_resources={
        #         "file_search": {
        #         "vector_store_ids": [created_vector_store_id]
        #         }
        #     }
        # )
                
        my_thread = client.beta.threads.create()
        
        print(f"New thread is created \n{my_thread}")  # Debugging line
        
        # save new thread id to file for loading in the next time
        write_dictionary(my_thread.model_dump(), thread_file)
        print(f"Saved the Thread ID = {my_thread.id}")  # Debugging line            
    else:
        # retrieve thread if it has been already created
        my_thread = client.beta.threads.retrieve(starting_thead_id)
    
    return my_thread

# Create a message, run the assistant on it, monitor it for completion, and display the output
def run_assistant(message_body, thread_id, assistant_id):
    # Create a message in an existing thread
    message = client.beta.threads.messages.create(
        thread_id = thread_id,
        role="user",
        content=message_body             
    )
    
    print("Created message:")
    print(f"{message.model_dump_json()}")
    
    # Run the existing assistant on the existing thread
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,               
    )
    
    print("Created run: ")
    print(f'{run.model_dump_json()}')
    
    
    print("Retrieving the response...")
    # Monitor the assistant and report status
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        time.sleep(.5)
    
    # Extract the messages from the thread
    messages = client.beta.threads.messages.list(
        thread_id=thread_id,
        run_id=run.id
    )
    
    # Display the output
    for message in reversed(messages.data):
        print(message.role + ": " + message.content[0].text.value)
    return messages
    
    
def start_conversation(thread_id, assistant_id):
    while True:
        user_input = input("Enter a question, or type 'exit' to end: ").strip().lower()
        if user_input == 'exit':
            break
        else:
            print(f"Received question: {user_input}")
            print(f"running the assistant to find the answer...")
            run_assistant(user_input, thread_id, assistant_id)


def main():
    
    # Print the current OpenAI SDK version
    current_version = version.parse(openai.__version__)
    print(f"Using OpenAI SDK version {current_version}")  # Debugging line
    
    # Step 1: Create a new Assistant with File Search Enabled
    print(f"Step 1: Createing a new Assistant with File Search Enabled")  # Debugging line        
    my_assistant = create_assistant()

    # Step 2: Upload files and add them to a Vector Store
    print(f"Step 2: Uploading files and add them to a Vector Store")  # Debugging line    
    
    file_paths = ["uploads/company-policy.md"]
    my_vector_store = create_vector_store(file_paths)
    save_uploaded_files(my_vector_store.id)
    
    # Step 3: Update the assistant to to use the new Vector Store
    print(f"Step 3: Updating the assistant to to use the new Vector Store")  # Debugging line    
    attached_assistant = attach_vector_store_to_assistant(my_assistant, my_vector_store.id)
    
    # Step 4: Create a thread
    print(f"Step 4: Creating a thread")  # Debugging line        
    my_thread = create_thread()
    
    # Step 5: Create a run and check the output
    print(f"Step 4: Creating a run and check the output")  # Debugging line
    start_conversation(my_thread.id, my_assistant.id)
    
if __name__=="__main__":
    main()