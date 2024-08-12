"""Assistants API"""
import os
from flask import Blueprint, jsonify, request, current_app
from ..config import Config
from ..utils import dict_helper
from openai import OpenAI
import tiktoken
import traceback

blueprint_assistant = Blueprint(name="blueprint_assistant", import_name=__name__)

@blueprint_assistant.route('/retrieveassistant', methods=['POST'])
def retrieve_assistant():
    current_app.logger.info("Processing /retrieve API...")    
    
    try:
        data = request.get_json()

        if "api_key" not in data:
            return jsonify({"error": "API key is missing"}), 400

        api_key = data["api_key"]
        client = OpenAI(api_key=api_key)

        # Retrieve an Assistant Object
        assistant_id = data["assistant_id"]
        assistant_response = client.beta.assistants.retrieve(assistant_id=assistant_id)
        
        # Extract the vector_store_id from Assistant Object
        assistant_model = assistant_response.model_dump()
        
        vector_store_ids = dict_helper.deep_get(assistant_model, ['tool_resources', 'file_search', 'vector_store_ids'], default=None)
        vector_store_id = vector_store_ids[0] if vector_store_ids is not None and len(vector_store_ids) > 0 else None
        
        # Checking FileSearch is enabled
        file_search_enabled = False
        tools_list = dict_helper.deep_get(assistant_model, ['tools'], default=None)
        if tools_list is not None and len(tools_list) > 0:
            for tool_item in tools_list:
                tool_type = dict_helper.deep_get(tool_item, ['type'], default="")
                if tool_type == "file_search":
                    file_search_enabled = True
                    break          
        
        current_app.logger.info(f"Returned Assistant object \n{assistant_model}")
        return jsonify(
            {
                "assistant_object": assistant_response.model_dump(),
                "vector_store_id": vector_store_id,
                "file_search_enabled": file_search_enabled
            }
        )

    except Exception as e:
        tb = traceback.format_exc()
        current_app.logger.error('API /retrieve error: \n%s', tb)
        return jsonify({"error": str(e)}), 500    

@blueprint_assistant.route('/createassistant', methods=['POST'])
def create_assistant():
    current_app.logger.info("Processing /createassistant API...")
    #current_app.logger.info(f"Flask secret key: {Config.FLASK_SECRET_KEY}") 
    #output = {"msg": "Assistant has been created"}
    #return jsonify(output)
    try:
        data = request.get_json()

        if "api_key" not in data:
            return jsonify({"error": "API key is missing"}), 400

        api_key = data["api_key"]
        client = OpenAI(api_key=api_key)

        # Create an Assistant
        model = Config.OPENAI_MODEL_NAME
        response = client.beta.assistants.create(
                        model = model
                    )
        
        current_app.logger.info(f"New ASSISTANT has been created with Id = {response.id}")
        return jsonify({"assistant_id": response.id})

    except Exception as e:
        tb = traceback.format_exc()
        current_app.logger.error('API /createassistant error: \n%s', tb)
        return jsonify({"error": str(e)}), 500

@blueprint_assistant.route('/createthread', methods=['POST'])
def create_thread():
    current_app.logger.info("Processing /createhread API...")
    #output = {"msg": "Thread has been created"}
    #return jsonify(output)
    
    try:
        data = request.get_json()

        if "api_key" not in data:
            return jsonify({"error": "API key is missing"}), 400

        api_key = data["api_key"]
        client = OpenAI(api_key=api_key)

        # Create a Thread
        my_thread = client.beta.threads.create()
        
        current_app.logger.info(f"New THREAD has been created with Id = {my_thread.id}")
        return jsonify({"thread_id": my_thread.id})

    except Exception as e:
        tb = traceback.format_exc()
        current_app.logger.error('API /createthread error: \n%s', tb)
        return jsonify({"error": str(e)}), 500

@blueprint_assistant.route('/ask', methods=['POST'])
def ask_question():
    current_app.logger.info("Processing /ask API...")
    #output = {"answer": "This is the answer message for your question - L1"}
    #return jsonify(output)
    
    try:
        data = request.get_json()

        if "api_key" not in data:
            return jsonify({"error": "API key is missing"}), 400

        api_key = data["api_key"]
        client = OpenAI(api_key=api_key)

        assistant_id = data["assistant_id"]

        thread_id =  data["thread_id"]

        question = data["question"]        
    except Exception as e:
        tb = traceback.format_exc()
        current_app.logger.error('L1 /ask error: \n%s', tb)
        return jsonify({"error": str(e)}), 500

    try:
        # Using Chat Completion - None Conversation Based
        # response = client.chat.completions.create(
        #     model=model,
        #     messages=[
        #         {"role": "user", "content": question}
        #     ],
        #     max_tokens=150
        # )
        # return jsonify({"answer": response.choices[0].message.content})

        # Using Threads Messages - Conversation Based        
        my_thread_message = client.beta.threads.messages.create(
            thread_id = thread_id,
            role = "user",
            content = question,
        )
        current_app.logger.info(f"New MESSAGE has been created with Id = {my_thread_message.id} on THREAD Id ={thread_id}")

        # Count input tokens
        model = Config.OPENAI_MODEL_NAME
        encoding = tiktoken.encoding_for_model(model)
        input_tokens = encoding.encode(question)
        input_token_count = len(input_tokens)

        # Run the existing assistant on the existing thread
        my_run = client.beta.threads.runs.create(
            thread_id = thread_id,
            assistant_id = assistant_id,
            instructions = "Emteller Chatbot. Xin chào bạn!"
        )
        current_app.logger.info(f"New RUN has been created with Id = {my_run.id} on THREAD Id = {thread_id} and ASSISTANT Id = {assistant_id}")

        # Monitor the assistant and report status
        while my_run.status != "completed":
            my_run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=my_run.id
                )
            
            current_app.logger.debug(f"My run {my_run.id} has status: {my_run.status}")
            if my_run.status == "failed" :
                break

        # Extract the messages from the thread
        if my_run.status != "failed" :
            messages =  client.beta.threads.messages.list(
                thread_id=thread_id,
                run_id=my_run.id
                )

        output_tokens = encoding.encode(messages.data[0].content[0].text.value)
        output_token_count = len(output_tokens)

        json_data = {
            "input_token_count" : input_token_count,
            "output_token_count" : output_token_count,
            "assistantID": assistant_id,
            "answer": messages.data[0].content[0].text.value
        }

        return jsonify(json_data),200

    except Exception as e:
        tb = traceback.format_exc()
        current_app.logger.error('L1 /ask error: \n%s', tb)
        return jsonify({"error": str(e)}), 500        

@blueprint_assistant.route('/askl22', methods=['POST'])
def ask_question_l22():
    current_app.logger.info("Processing /askl22 API...")
    #output = {"answer": "This is the answer message for your question - L22"}
    #return jsonify(output)
    
    try:
        data = request.get_json()

        if "api_key" not in data:
            return jsonify({"error": "API key is missing"}), 400

        api_key = data["api_key"]

        # 1st solution - fit file to assistantId
        client = OpenAI(api_key=api_key)
        thread_id =  data["thread_id"]

        # 2nd solution - load file from intent store
        # openai_model = create_openai_api(OPENAI_API_KEY = api_key)

        assistant_id = data["assistant_id"]

        question = data["question"]
    except Exception as e:
        tb = traceback.format_exc()
        current_app.logger.error('L22 /askl22 error: \n%s', tb)
        return jsonify({"error": str(e)}), 500
    
    
    try:
        # 1st solution
        prompt = question

        # prompt = instruction_assis
        # prompt = prompt.replace("{question}", question)

        my_thread_message = client.beta.threads.messages.create(
            thread_id = thread_id,
            role = "user",
            content = prompt,
        )
        current_app.logger.info(f"New MESSAGE has been created with Id = {my_thread_message.id} on THREAD Id ={thread_id}")

        # Count input tokens
        model = Config.OPENAI_MODEL_NAME
        encoding = tiktoken.encoding_for_model(model)
        input_tokens = encoding.encode(prompt)
        input_token_count = len(input_tokens)

        thread_run = client.beta.threads.runs.create(
            thread_id= thread_id,
            assistant_id=assistant_id,
        )
        current_app.logger.info(f"New RUN has been created with Id = {thread_run.id} on THREAD Id = {thread_id} and ASSISTANT Id = {assistant_id}")

        while thread_run.status in ["queued", "in_progress"]:
            keep_retrieving_run = client.beta.threads.runs.retrieve(
                thread_id= thread_id,
                run_id= thread_run.id
            )
            
            current_app.logger.debug(f"My run {keep_retrieving_run.id} has status: {keep_retrieving_run.status}")

            if keep_retrieving_run.status == "completed":
                all_messages = client.beta.threads.messages.list(
                    thread_id= thread_id
                )

                # print("\n------------------------------------------------------------ \n")
                # print(f"\nUser: {my_thread_message.content[0].text.value}")
                # print(f"\nAssistant: {all_messages.data[0].content[0].text.value}")

                break
            elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
                pass
            else:
                break

        output_tokens = encoding.encode(all_messages.data[0].content[0].text.value)
        output_token_count = len(output_tokens)

        json_data = {
            "input_token_count" : input_token_count,
            "output_token_count" : output_token_count,
            "assistantID": assistant_id,
            "answer": all_messages.data[0].content[0].text.value
        }        

        # 2nd solution
        # try:
        #     filename = os.path.join(os.environ['INTENT_STORE'], assistant_id)
        #     with open(filename, "r") as f:
        #         text = f.read()
        # except Exception as ef:
        #     return jsonify({"error": str(ef)}), 500

        # prompt = instruction
        # prompt = prompt.replace("{text}", text)
        # prompt = prompt.replace("{question}", question)
        # answer = call_openai_api(openai_model, prompt)

        # json_data = {
        #     "assistantID": assistant_id,
        #     "answer": answer
        # }

        return jsonify(json_data), 200

    except Exception as e:
        tb = traceback.format_exc()
        current_app.logger.error('L22 /askl22 error: \n%s', tb)
        return jsonify({"error": str(e)}), 500
    