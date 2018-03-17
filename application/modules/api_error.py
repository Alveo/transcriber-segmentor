from flask import jsonify

def api_error(message):
    return jsonify({'error': True, 'code': 400, 'message': message})
