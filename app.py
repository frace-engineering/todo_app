#!/usr/bin/python3
from flask import Flask, jsonify, abort, make_response, request
""" Flask was imported to build the flask api.
    jsonify was imported to render response in json format.
    abort was imported to abort processing due to any error.
    make_response was imported to help convert html format to json format.
    request was imported to update and create new task
    """

app = Flask(__name__)

tasks = [
        {
            'id': 1,
            'title': 'Buy groceries',
            'description': 'Milk, Cheese, Pizza',
            'done': False
            },
        {
            'id': 2,
            'title': u'Learn Python',
            'description': u'Need to find a good Python turtorial',
            'done': False
            }
        ]
@app.route("/todo/api/v1.0/tasks", methods=['GET'], strict_slashes=False)
def get_task():
    return jsonify({'tasks': tasks})

@app.route("/friday", strict_slashes=False)
def index():
    return "http://www.enugudisco.com"

@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods=['GET'], strict_slashes=False)
def get_task_id(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
            'id': tasks[-1]['id'] + 1,
            'title': request.json['title'],
            'description':request.json.get('description'),
            'done': False
            }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'decription' in request.json and type(request.json['description']) != unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task':task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': 'Deleted'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
