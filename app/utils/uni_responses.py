from flask import jsonify
from flask_smorest import abort


def invalid_id_response(_id: int, cls: str):
    """UniversalResponse for invalid id request"""
    return abort(400, message=f"Invalid {cls} id {_id} or {cls} was deleted")


def success_response():
    """Success message response"""
    return jsonify({"message": "Success"}), 200

