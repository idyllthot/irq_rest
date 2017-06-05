#!/usr/bin/env python
# Filename irq_rest_server.py

""" REST API service for identifying IRQs and values for CPU0,CPU1 """

__author__ = "Adam R. Dalhed"
__version__ = "0.0.1"

from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

auth = HTTPBasicAuth()

e = create_engine('sqlite:///irq.db')

app = Flask(__name__)

api = Api(app)

class Irqs_Meta(Resource):
    def get(self):
        #Connect to databse
        conn = e.connect()
        #Perform query and return JSON data
        query = conn.execute("select distinct id from irqs")
        return {'irq': [i[0] for i in query.cursor.fetchall()]}

class Irqs_Info(Resource):
	def get(self,id):
		conn = e.connect()
		#Perform query and return JSON data
		query = conn.execute("select * from irqs where id='%s'" %id)
        	#Query the result and get cursor.Dumping that data to a JSON is looked by extension
        	result = {'irq': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        	return result
        	#We can have PUT,DELETE,POST here. But in our API GET implementation is sufficient
 
api.add_resource(Irqs_Info, '/irq/<int:id>')
api.add_resource(Irqs_Meta, '/irq')

if __name__ == '__main__':
        app.run(debug=True,host="0.0.0.0",port=21973)

'''

@auth.get_password
def get_password(username):
	if username == 'vdms':
		return 'edgy'
	return None

@auth.error_handler
def unauthorized():
	return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
	#return jsonify({'tasks': tasks})
	return jsonify({'tasks': [make_public_task(task) for task in tasks]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
	task = [task for task in tasks if task['id'] == task_id]
	if len(task) == 0:
		abort(404)
	return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@auth.login_required
def create_task():
	if not request.json or not 'title' in request.json:
		abort(400)
	task = {
		'id': tasks[-1]['id'] + 1,
		'title': request.json['title'],
		'description': request.json.get('description', ""),
		'done': False
	}
	tasks.append(task)
	return jsonify({'task': task}), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

def make_public_task(task):
	new_task = {}
	for field in task:
		if field == 'id':
			new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
		else:
			new_task[field] = task[field]
	return new_task


if __name__ == '__main__':
	app.run(debug=True,host="0.0.0.0",port=21973)

'''
