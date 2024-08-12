"""Assistants API"""
import os
from flask import Blueprint, jsonify, request, current_app
from ..config import Config

from openai import OpenAI
import tiktoken
import traceback

blueprint_assistant = Blueprint(name="blueprint_assistant", import_name=__name__)

@blueprint_assistant.route('/createassistant', methods=['POST'])
def create_assistant():
    current_app.logger.info("Processing /createassistant API...")
    current_app.logger.info(f"Flask secret key: {Config.FLASK_SECRET_KEY}") 
    output = {"msg": "Assistant has been created"}
    return jsonify(output)

@blueprint_assistant.route('/createthread', methods=['POST'])
def create_thread():
    current_app.logger.info("Processing /creathread API...")
    output = {"msg": "Thread has been created"}
    return jsonify(output)

@blueprint_assistant.route('/ask', methods=['POST'])
def ask_question():
    current_app.logger.info("Processing /ask API...")
    output = {"answer": "This is the answer message for your question - L1"}
    
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

        # Monitor the assistant and report status
        while my_run.status != "completed":
            my_run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=my_run.id
                )
            
            current_app.logger.info(f"Run status: {my_run.status}")            
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
    output = {"answer": "This is the answer message for your question - L22"}
    return jsonify(output)