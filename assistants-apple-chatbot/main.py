import os
import json
from time import sleep
from packaging import version
from flask import Flask, request, Response, jsonify
import openai
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Check OpenAI version is correct. Require using V1 SDK
min_required_version = version.parse("1.1.1")
max_required_version = version.parse("1.20.0")
current_version = version.parse(openai.__version__)
print(f"Using OpenAI SDK version {current_version}")  # Debugging line
if (current_version< min_required_version or current_version > max_required_version):
    raise ValueError(f"Error: OpenAI version {openai.__version__}"
                     " is less than the required version 1.1.1")
else:
    print("OpenAI version is compatible.")

# Start Flask app
app = Flask(__name__)

# Init client
client = OpenAI(
    api_key=OPENAI_API_KEY # should use env variable OPENAI_API_KEY in secrets (bottom left corner)
)

# Start conversation thread
@app.route('/start', methods=['GET'])
def start_conversation():
    print(f"Starting a new conversation...")  # Debugging line
    thread = client.beta.threads.create()
    print(f"New thread created with ID: {thread.id}")  # Debugging line
    return jsonify({"thread_id": thread.id})

# Generate response
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    
    assistant_id = data.get("assistant_id")
    thread_id = data.get('thread_id')
    user_input = data.get('message', '')
    
    if not assistant_id:
        print(f"Error: Missing assistant_id")  # Debugging line
        return jsonify({"error": "Missing assistant_id"}), 400
    
    if not thread_id:
        print(f"Error: Missing thread_id")  # Debugging line
        return jsonify({"error": "Missing thread_id"}), 400
    
    print(f"Received message: {user_input} for thread ID: {thread_id}")  # Debugging line
    
    # Add the user's message to the thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input
        )
    
    # Run the Assistant
    print(f"Run the received message on Assistant ID: {assistant_id}")  # Debugging line
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    
    # Check if the Run requires action (function call)
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        
        print(f"Run status: {run_status.status}")  # Debugging line
        
        if run_status.status == 'completed':
            break
        
        sleep(1)  # Wait for a second before checking again
    
    # Retrieve and return the latest message from the assistant
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    response = messages.data[0].content[0].text.value
    
    print(f"Assistant response: {response}")  # Debugging line
    return jsonify({"response": response})


#####################
# Common Functions
#####################
def create_result_model(success, code, message, data):
    return {"success": success,"code": code, "message": message, "data": data}

@app.route('/manage/ping', methods=['GET'])
def helloworld():
    return "PONG", 200


#####################
# Assistants API
#####################
@app.route('/manage/assistants', methods=['GET','POST'])
def all_assistant():
    
     # Starting process request    
    try:
        
        # Log request event
        print(f"Assistant all requesting: [{request.method}]")  # Debugging line
        print(request.query_string)        
        if request.content_length is not None and request.content_length > 0:     
            request_body = request.get_json()
            print(request_body)
        

        # Get all assistants
        if request.method == 'GET':
            order = request.args.get('order')
            limit = request.args.get('limit')
            all_assistants_reponse = client.beta.assistants.list(order=order, limit=limit)
            result = create_result_model(True, 1, "OK", all_assistants_reponse.model_dump())
            return jsonify(result),200


        # Create new assistant
        if request.method == 'POST':
            
            # Create new assistant on OpenAI
            create_assistant_response = client.beta.assistants.create(
                name=request_body['name'],
                description=request_body['description'],
                instructions=request_body['instructions'],
                model="gpt-3.5-turbo",
                tools=[{"type": "retrieval"}],
                file_ids=request_body['file_ids']
            )
            print(create_assistant_response)
            print(f"Assistant created successfully with ID: {create_assistant_response.id}")   # Debugging line                        
                
            # Save the uploaded result
            kbfile_file_path = f"saved/assistant_{create_assistant_response.id}.json"
            with open(kbfile_file_path, 'w') as file:                               
                json.dump(create_assistant_response.model_dump(), file)
                print(f"Saved the Assistant ID = {create_assistant_response.id}")  # Debugging line
            
            # Return response
            result = create_result_model(True, 1, "OK", create_assistant_response.model_dump())
            return jsonify(result),200                
            

        # Other not implemented cases                
        result = create_result_model(False, -998, "Not implemented", None)
        return jsonify(result), 404
    
    except Exception as ex:
        print(f"{ex}")  # Debugging line
        result = create_result_model(False, -999, str(ex), None)
        return jsonify(result), 500
  

@app.route('/manage/assistants/<string:key>', methods=['GET','PUT','DELETE'])
def single_assistant(key):
    
    # Starting process request    
    try:
        
        # Log request event
        print(f"Assistant single requesting: [{request.method}] Key={key}")  # Debugging line
        print(f"[{request.method}] - {request.url}")        
        if request.content_length is not None and request.content_length > 0:        
            request_body = request.get_json()
            print(request_body)
        
        # Retrieve the assistant object
        if request.method == "GET":            
            assistant_retrieve_response = client.beta.assistants.retrieve(assistant_id=key)
            result = create_result_model(True, 1, "OK", assistant_retrieve_response.model_dump())
            return jsonify(result),200
        
        # Modify assistant object
        if request.method == "PUT":
            
            print(f"Updating assistant with ID: {key} ...")  # Debugging line            
            # Build the dictionary of changes  
            changes_dict = {}     
            if request_body['name'] is not None:
                changes_dict["name"] = request_body['name']
            if request_body['description'] is not None:
                changes_dict["description"] = request_body['description']                                            
            if request_body['file_ids'] is not None:
                changes_dict['file_ids'] = request_body['file_ids']
            if request_body['instructions'] is not None:
                changes_dict['instructions'] = request_body['instructions']
                
            # Update the assistant to OpenAI
            print(changes_dict)
            client.beta.assistants.update(assistant_id=key, **changes_dict)
            
            # Return result response
            result = create_result_model(True, 1, f"The assistant with ID: {key} is updated successfully", None)
            return jsonify(result), 200
        
        # Delete assistant
        if request.method == "DELETE":
            client.beta.assistants.delete(key)
            result = create_result_model(True, 1, f"The assistent with ID: {key} is deleted successfully", None)
            return jsonify(result), 200
        
        
        # Other not implemented cases
        result = create_result_model(False, -998, "Not implemented", None)
        return jsonify(result), 404
    except Exception as ex:
        print(f"{ex}")  # Debugging line
        result = create_result_model(False, -999, str(ex), None)
        return jsonify(result), 500    


#####################
# Threads API
#####################
@app.route('/manage/threads', methods=['GET','POST'])
def all_thread():
    
     # Starting process request    
    try:
        
        # Log request event
        print(f"Threads all requesting: [{request.method}]")  # Debugging line
        print(request.query_string)        
        if request.content_length is not None and request.content_length > 0:     
            request_body = request.get_json()
            print(request_body)        

        # Create new assistant
        if request.method == 'POST':
            
            # Create new thread on OpenAI
            create_thread_response = client.beta.threads.create()
            
            print(create_thread_response)
            print(f"Thread created successfully with ID: {create_thread_response.id}")   # Debugging line                        
                
            # Save the uploaded result
            kbfile_file_path = f"saved/thread_{create_thread_response.id}.json"
            with open(kbfile_file_path, 'w') as file:                               
                json.dump(create_thread_response.model_dump(), file)
                print(f"Saved the Thread ID = {create_thread_response.id}")  # Debugging line
            
            # Return response
            result = create_result_model(True, 1, "OK", create_thread_response.model_dump())
            return jsonify(result),200                
            

        # Other not implemented cases                
        result = create_result_model(False, -998, "Not implemented", None)
        return jsonify(result), 404
    
    except Exception as ex:
        print(f"{ex}")  # Debugging line
        result = create_result_model(False, -999, str(ex), None)
        return jsonify(result), 500
  

@app.route('/manage/threads/<string:key>', methods=['GET','PUT','DELETE'])
def single_thread(key):
    
    # Starting process request    
    try:
        
        # Log request event
        print(f"Thread single requesting: [{request.method}] Key={key}")  # Debugging line
        print(f"[{request.method}] - {request.url}")        
        if request.content_length is not None and request.content_length > 0:        
            request_body = request.get_json()
            print(request_body)
        
        # Retrieve the thread object
        if request.method == "GET":            
            thread_retrieve_response = client.beta.threads.retrieve(thread_id=key)
            result = create_result_model(True, 1, "OK", thread_retrieve_response.model_dump())
            return jsonify(result),200
                
        # Delete thread
        if request.method == "DELETE":
            client.beta.threads.delete(key)
            result = create_result_model(True, 1, f"The thread with ID: {key} is deleted successfully", None)
            return jsonify(result), 200
        
        
        # Other not implemented cases
        result = create_result_model(False, -998, "Not implemented", None)
        return jsonify(result), 404
    except Exception as ex:
        print(f"{ex}")  # Debugging line
        result = create_result_model(False, -999, str(ex), None)
        return jsonify(result), 500  



#####################
# Files API
#####################
@app.route('/manage/files', methods=['GET','POST'])
def all_file():
    
     # Starting process request    
    try:
        
        # Log request event
        print(f"File all requesting: [{request.method}]")  # Debugging line
        print(request.query_string)        
        if request.content_length is not None and request.content_length > 0:     
            request_body = request.get_json()
            print(request_body)
        

        # Get all files
        if request.method == 'GET':            
            all_file_reponse = client.files.list()
            result = create_result_model(True, 1, "OK", all_file_reponse.model_dump())
            return jsonify(result),200
        

        # Create new file
        if request.method == 'POST':
            
            # Upload new file to OpenAI
            file_name = f"uploaded/{request_body['filename']}"
            with open(file_name, "rb") as file:                
                file_create_response = client.files.create(
                    file=file,
                    purpose='assistants'
                )
                print(file_create_response)
                print(f"File uploaded successfully: {file_create_response.filename} [{file_create_response.id}]")   # Debugging line
                
            # Save the uploaded result
            kbfile_file_path = f"saved/kbfile_{file_create_response.id}.json"
            with open(kbfile_file_path, 'w') as file:
                # json.dump({'file_id': kbfile_id}, file)
                # Save response to JSON file 
                json.dump(file_create_response.model_dump(), file)
                print(f"Saved the File ID = {file_create_response.id}")  # Debugging line
            
            # Return response
            result = create_result_model(True, 1, "OK", file_create_response.model_dump())
            return jsonify(result),200                       
            

        # Other not implemented cases                
        result = create_result_model(False, -998, "Not implemented", None)
        return jsonify(result), 404
    
    except Exception as ex:
        print(f"{ex}")  # Debugging line
        result = create_result_model(False, -999, str(ex), None)
        return jsonify(result), 500



@app.route('/manage/files/<string:key>', methods=['GET','PUT','DELETE'])
def single_file(key):    
    
    try:
    
        print(f"File requesting: [{request.method}] Key={key}")  # Debugging line  
        print(f"[{request.method}] - {request.url}")        
        if request.content_length is not None and request.content_length > 0:        
            request_body = request.get_json()
            print(request_body)
        
        # Retrieve the file object information
        if request.method == "GET":            
            file_retrieve_response = client.files.retrieve(file_id=key)
            result = create_result_model(True, 1, "OK", file_retrieve_response.model_dump())
            return jsonify(result), 200    
            """ response = Response(
                response=file_response.model_dump_json(),
                status=200,
                mimetype='application/json'
            )
            return response """
        
        # Delete the file from OpenAI
        if request.method == "DELETE":            
            client.files.delete(key)
            result = create_result_model(True, 1, f"The file ID: {key} is deleted successfully", None)
            return jsonify(result), 200
                              
        
        # Other not implemented cases
        result = create_result_model(False, -998, "Not implemented", None)
        return jsonify(result), 404
    
    except Exception as ex:
        print(f"{ex}")  # Debugging line
        result = create_result_model(False, -999, str(ex), None)
        return jsonify(result), 500


# Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)