from flask import Flask, jsonify

from src.server_data import users, tasks, users_score

app = Flask(__name__)


@app.route('/')
def home():
    return "API для взаимодействия с LMS системы"


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)


@app.route('/tasks/<direction>', methods=['GET'])
def get_tasks_by_direction(direction):
    if direction.upper() in tasks:
        return jsonify({
            "direction": direction,
            "tasks": tasks[direction]
        })
    return jsonify({"error": "Direction not found"}), 404


@app.route('/users/<string:name>', methods=['GET'])
def get_score(name):
    user = next((u for u in users_score if u['name'].lower() == name.lower()), None)

    if user:
        response = {
            "name": user["name"],
            "scores": {k: v for k, v in user.items() if k != "name"},
        }
        return jsonify(response)

    return jsonify({"error": "User not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
