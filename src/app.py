"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def show_all_members():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members,
        "status": "ok"
    }
    return jsonify(response_body), 200

@app.route('/members/<int:member_id>', methods=['GET'])
def show_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"status": "lo siento pana, not found"}), 404

@app.route('/members', methods=['POST'])
def add_member():
    request_body = request.get_json()
    
    if not request_body:
        return jsonify({"status": "Alto ahí! bad request"}), 400
    
    required_fields = ["first_name", "age", "lucky_numbers"]
    for field in required_fields:
        if field not in request_body:
            return jsonify({"status": f"{field} se NECESITA"}), 400
    
    jackson_family.add_member(request_body)
    return jsonify({"status": "Parecen conejos, cómprense una tele"}), 200

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    if jackson_family.delete_member(member_id):
        return jsonify({"done": True}), 200
    else:
        return jsonify({"status": "member not found"}), 404

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
