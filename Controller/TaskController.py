from EntityModel.CompositeTask import CompositeTask
from EntityModel.SimpleTask import SimpleTask
from EntityModel.Deliverable import Deliverable
from flask import Flask, jsonify, request
import main_func
import json
import os.path
import sys

def createTask(name, duration, tsktype, children, pred, succ, resources, desc, parentId, deliverables):
	

	if(tsktype == "SimpleTask"):
	    newTask = SimpleTask(main_func.getId(), name, desc, None, duration, pred, succ, resources, deliverables)
	else:
	    startTask = None
	    finalTasks = []
	    newTask = CompositeTask(main_func.getId(), name, desc, None, duration, startTask, finalTasks, pred, succ, [], resources, deliverables)
	
	if(parentId in main_func.project_objects):
	    parentTask = main_func.project_objects[parentId]
	    parentTask.addChildTask(newTask)

	newTask_json = main_func.jdefault(newTask)
	project_json = None
 	with open(os.path.join(sys.path[0]+'/static/data', 'Project.json'), 'r') as inFile:
		project_json = json.load(inFile);

	if children:
		taskList = project_json['children']
		newTask_json['children'] = [task for task in taskList if task['id'] in children]
		project_json['children'] = [task for task in taskList if task['id'] not in children]

	project_json['children'].append(newTask_json);

	if resources:
		resList = project_json['resources']
		for resource in resList:
			if resource['id'] in resources:
				resource['allocTasks'].append(newTask.id)

	if pred:
		taskList = project_json['children']
		for task in taskList:
			if task['id'] in pred:
				task['succ'].append(newTask.id)

	if succ:
		taskList = project_json['children']
		for task in taskList:
			if task['id'] in succ:
				task['pred'].append(newTask.id)

	with open(os.path.join(sys.path[0]+'/static/data', 'Project.json'), 'w') as outFile:
		json.dump(project_json, outFile)

	return json.dumps(project_json, default=main_func.jdefault, indent = 2)

def editTask(id, name, duration, tsktype, children, pred, succ, resources, desc, parentId, deliverables):

	project_json = None
 	with open(os.path.join(sys.path[0]+'/static/data', 'Project.json'), 'r') as inFile:
		project_json = json.load(inFile);

	taskList = project_json['children']
	old_task = findTask(id,taskList)

	if(tsktype == "SimpleTask"):
	    newTask = SimpleTask(id, name, desc, old_task['date'], duration, pred, succ, resources, deliverables)
	else:
	    startTask = None
	    finalTasks = []
	    if old_task.has_key('startTask'):
	    	startTask = old_task['startTask']
	    if old_task.has_key('finalTasks'):
	    	finalTasks = old_task['finalTasks']
	    newTask = CompositeTask(id, name, desc, old_task['date'], duration, startTask, finalTasks, pred, succ, [], resources, deliverables)
	
	newTask_json = main_func.jdefault(newTask)
	if old_task.has_key('children'):
		if (tsktype == "CompositeTask"):
			newTask_json['children'] = [task for task in old_task['children'] if task['id'] in children]
			taskList.extend([task for task in old_task['children'] if task['id'] not in children])

		else:
			taskList.extend([task for task in old_task['children']])

	if children:
		newTask_json['children'].extend([task for task in taskList if task['id'] in children])
		taskList = [task for task in taskList if task['id'] not in children]

	resList = project_json['resources']
	for resource in resList:
		if resource['id'] in resources and id not in resource['allocTasks']:
			resource['allocTasks'].append(id)
		elif resource['id'] not in resources and id in resource['allocTasks']:
			resource['allocTasks'].remove(id)

	for task in taskList:
		if task['id'] in pred and id not in task['succ']:
			task[succ].append(id)
		elif task['id'] not in pred and id in task['succ']:
			task[succ].remove(id) 

	for task in taskList:
		if task['id'] in succ and id not in task['pred']:
			task[pred].append(id)
		elif task['id'] not in succ and id in task['pred']:
			task[pred].remove(id)

	replaceTask(id,taskList,newTask_json)

	project_json['children'] = taskList
	with open(os.path.join(sys.path[0]+'/static/data', 'Project.json'), 'w') as outFile:
		json.dump(project_json, outFile)

	return json.dumps(project_json, default=main_func.jdefault, indent = 2)	

def findTask(id,taskList):
	for task in taskList:
		if task['id'] == id:
			return task
		if task.has_key('children'):
			children = task['children']
			if children:
				tsk = findTask(id,children)
				if tsk is not None:
					return tsk
	return None

def replaceTask(id,taskList,newTask):
	for task in taskList:
		if task['id'] == id:
			taskList.remove(task)
			taskList.append(newTask)
			print newTask
			return
		if task.has_key('children'):
			children = task['children']
			if children:
				replaceTask(id,children,newTask)
