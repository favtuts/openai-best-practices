from flask import Blueprint, jsonify, request

blueprint_testing = Blueprint(name="blueprint_testing", import_name=__name__)

x = 5
y = 1000

@blueprint_testing.route('/test', methods=['GET'])
def test():
    """
    ---
    get:
      description: test endpoint
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: OutputSchema
      tags:
          - testing
    """
    output = {"msg": "I'm the test endpoint from blueprint_testing."}
    return jsonify(output)


@blueprint_testing.route('/plus', methods=['POST'])
def plus_x():
    """
    ---
    post:
      description: increments the input by x
      requestBody:
        required: true
        content:
            application/json:
                schema: InputSchema
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: OutputSchema
      tags:
          - calculation
    """
    # retrieve body data from input JSON
    data = request.get_json()
    in_val = data['number']
    # compute result and return as JSON
    result = in_val + x
    output = {"msg": f"Your result is: '{result}'"}
    return jsonify(output)


@blueprint_testing.route('/minus', methods=['POST'])
def minus_y():
    """
    ---
    post:
      description: decrements the input by x
      requestBody:
        required: true
        content:
            application/json:
                schema: InputSchema
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: OutputSchema
      tags:
          - calculation
    """
    # retrieve body data from input JSON
    data = request.get_json()
    in_val = data['number']
    # comput result and output as JSON
    result = in_val - y
    output = {"msg": f"Your result is: '{result}'"}
    return jsonify(output)
