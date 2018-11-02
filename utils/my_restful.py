from flask import jsonify

class Code:
    SUCCESS = 200
    PARAM_ERROR = 400
    AUTH_ERROR = 401
    SERVER_ERROR = 500

def result(code, message, data={}):
    return jsonify({"code": code, "message": message, "data": data})