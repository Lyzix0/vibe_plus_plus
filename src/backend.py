from flask import Flask, request, jsonify

from src.server_data import users, tasks

app = Flask(__name__)


@app.route('/')
def home():
    return "API для взаимодействия с LMS системы"


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "Пользователь не найден"}), 404


@app.route('/tasks/<direction>', methods=['GET'])
def get_tasks_by_direction(direction):
    if direction.upper() in tasks:
        return jsonify({
            "direction": direction.upper(),
            "tasks": tasks[direction.upper()]
        })
    return jsonify({"error": "Direction not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
