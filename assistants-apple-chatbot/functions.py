import json
import os

def create_assistant(client):
    assistant_file_path = 'saved_assistant.json'   
    
    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, 'r') as file:
            assistant_data = json.load(file)
            assistant_id = assistant_data['assistant_id']
            print(f"Loaded existing assistant ID = {assistant_id}")
    else:
        
        created_kbfile_id = create_file(client)
        
        assistant = client.beta.assistants.create(
            instructions="""
          The assistant, Apple Assistant, has been programmed to help supporter reps with learning ompany standard operating procedures.
          A document has been provided with information on Apple processes and training info.
          """,            
            model="gpt-3.5-turbo",
            tools=[{"type": "retrieval"}],
            file_ids=[created_kbfile_id]
        )
        
        with open(assistant_file_path, 'w') as file:
            # json.dump({'assistant_id': assistant.id}, file)
            # Save response to JSON file 
            json.dump(assistant.json(), file)
            print(f"Created a new assistant and saved the ID = {assistant.id}")  # Debugging line
        
        assistant_id = assistant.id
    
    return assistant_id


def create_thread(client):
    thread_file_path = 'saved_thread.json'
    
    if os.path.exists(thread_file_path):
        with open(thread_file_path, 'r') as file:
            thread_data = json.load(file)
            thread_id = thread_data['thread_id']
            
            print(f"Loaded existing thread ID = {thread_id}")  # Debugging line
    else:
        thread = client.beta.threads.create()
        thread_id = thread.id
        print(f"New thread created with ID: {thread_id}")  # Debugging line
        
        with open(thread_file_path, 'w') as file:
            #json.dump({'thread_id': thread_id}, file)
            # Save response to JSON file 
            json.dump(thread.json(), file)
            print(f"Saved the Thread ID = {thread_id}")  # Debugging line
    
    return thread_id