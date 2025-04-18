from flask import Flask, jsonify

from src.server_data import users, tasks, users_score

app = Flask(__name__)


@app.route('/')
def home():
    return "API для взаимодействия с LMS системы"


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)


@app.route('/course_<int:course_number>/<string:direction>', methods=['GET'])
def get_tasks_by_course(course_number, direction):
    global tasks

    # Для 1 курса - общие задания
    if course_number == 1:
        data = tasks[1]["common"]
        response = {
            "course": course_number,
            "message": "Задания для первого курса",
            "tasks": data
        }
    else:
        data = tasks[course_number][direction]
        response = {
            "course": course_number,
            "direction": direction,
            "message": f"Задания для {direction}",
            "tasks": data
        }

    return jsonify(response)


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
