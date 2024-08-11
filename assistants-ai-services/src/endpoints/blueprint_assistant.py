"""Assistants API"""
from flask import Blueprint, jsonify, request

blueprint_assistant = Blueprint(name="blueprint_assistant", import_name=__name__)

@blueprint_assistant.route('/createassistant', methods=['POST'])
def create_assistant():
    output = {"msg": "Assistant has been created"}
    return jsonify(output)

@blueprint_assistant.route('/createthread', methods=['POST'])
def create_thread():
    output = {"msg": "Thread has been created"}
    return jsonify(output)

@blueprint_assistant.route('/ask', methods=['POST'])
def ask_question():
    output = {"answer": "This is the answer message for your question - L1"}
    return jsonify(output)

@blueprint_assistant.route('/askl22', methods=['POST'])
def ask_question_l22():
    output = {"answer": "This is the answer message for your question - L22"}
    return jsonify(output)