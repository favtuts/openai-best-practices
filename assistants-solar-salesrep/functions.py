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
          The assistant, Smith's Solar Sales Assistant, has been programmed to help junior sales reps with learning company standard operating procedures and selling techniques as a salesperson.
          A document has been provided with information on Smith's solars sales processes and training info.
          """,            
            model="gpt-3.5-turbo",
            tools=[{"type": "retrieval"}],
            file_ids=[created_kbfile_id]
        )
        
        with open(assistant_file_path, 'w') as file:
            json.dump({'assistant_id': assistant.id}, file)
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
    
    return thread_id

def create_file(client):
    kbfile_file_path = 'saved_kbfile.json'
    
    if os.path.exists(kbfile_file_path):
        with open(kbfile_file_path, 'r') as file:
            kbfile_data = json.load(file)
            kbfile_id = kbfile_data['file_id']
            
            print(f"Loaded existing file ID = {kbfile_id}")  # Debugging line
    else:
        file = client.files.create(
            file=open("knowledge.docx", "rb"),
            purpose='assistants'
        )                
        kbfile_id = file.id
        print(f"New file created with ID: {kbfile_id}")  # Debugging line
    
    return kbfile_id    