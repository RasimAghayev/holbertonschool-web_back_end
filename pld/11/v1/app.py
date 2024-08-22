#!/usr/bin/env python3
""" Task API
"""
from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from typing import List, Dict, Union

app = Flask(__name__)

# Configuring the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Task model with type declarations
class Task(db.Model):
    id: int = db.Column(db.Integer,
                        primary_key=True)  # Integer type for the primary key
    task: str = db.Column(
        db.String(200),
        nullable=False)  # String type with a max length of 200 characters

    def to_dict(self) -> Dict[str, Union[int, str]]:
        return {'id': self.id, 'task': self.task}


# Create the database and table
with app.app_context():
    db.create_all()


# Route to retrieve all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks() -> Response:
    tasks: List[Task] = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])


# Route to add a new task
@app.route('/tasks', methods=['POST'])
def add_task() -> Response:
    task_data: Dict[str, str] = request.get_json()
    if not task_data or 'task' not in task_data:
        return jsonify({'error': 'Invalid task data'}), 400

    task: Task = Task(task=task_data['task'])
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


# Route to delete a task by its ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int) -> Response:
    task: Task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'}), 200


if __name__ == '__main__':
    app.run(debug=True)
