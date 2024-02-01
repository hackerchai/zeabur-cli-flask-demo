from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
import os
import logging

app = Flask(__name__)
db_url = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'mysql://username:password@localhost/db_name'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(80), nullable=False)

@app.route('/tasks', methods=['POST'])
def add_task():
    content = request.json['content']
    task = Task(content=content)
    db.session.add(task)
    db.session.commit()
    return {'id': task.id}

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return {'tasks': [{'id': task.id, 'content': task.content} for task in tasks]}

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return {'result': 'success'}
    return {'result': 'error', 'message': 'Task not found'}, 404

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000), host='0.0.0.0')
