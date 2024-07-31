import os
from time import sleep
from packaging import version
from flask import Flask, request, jsonify
import openai
from openai import OpenAI
import functions

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

# Create new assistant or load existing
assistant_id = functions.create_assistant(client)

# Create default thread or load existing
thread_id = functions.create_thread(client)

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
    thread_id = data.get('thread_id')
    user_input = data.get('message', '')
    
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


# Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
        