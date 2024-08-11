"""System Information"""
from flask import Blueprint, jsonify, request

blueprint_systeminfo = Blueprint("blueprint_systeminfo", import_name=__name__)

@blueprint_systeminfo.route('/healthcheck', methods=['GET'])
def health_check():
    output = {"msg": "I'm the health_check endpoint from blueprint_systeminfo."}
    return jsonify(output)

@blueprint_systeminfo.route('/versioncheck', methods=['GET'])
def system_info():
    output = {"msg": "Assistant API V2"}
    return jsonify(output)