from flask import Blueprint, jsonify, request
from services import TaskService

task_blueprint = Blueprint('tasks', __name__)


@task_blueprint.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = TaskService.get_all_tasks()
    return jsonify(tasks), 200


@task_blueprint.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_id(task_id: int):
    task = TaskService.get_task_by_id(task_id)
    return jsonify(task), 200


@task_blueprint.route('/tasks', methods=['POST'])
def add_task():
    task_data = request.get_json()
    if not task_data or 'task' not in task_data:
        return jsonify({'error': 'Invalid task data'}), 400

    task = TaskService.add_task(task_data)
    return jsonify(task), 201


@task_blueprint.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int):
    success = TaskService.delete_task(task_id)
    if success:
        return jsonify({'message': 'Task deleted'}), 200
    return jsonify({'error': 'Task not found'}), 404
