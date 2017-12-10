import os
import sys
import time
import datetime
from pymongo import MongoClient

def new_task(task_id, workflow, timestamp, comment, code):
    document = {
        "task_id" : task_id,
        "workflow" : workflow,
        "timestamp" : timestamp,
        "comment" : comment,
        "code" : code
    }
    client = MongoClient()
    db = client.helix
    return db.runningtask.insert_one(document).inserted_id

def update_task_state(task_id, state, stage, msg):
    client = MongoClient()
    db = client.helix    
    db.runningtask.update_one({'task_id': task_id}, {'$set': {'state' : state, 'stage' : stage, 'stage_message' : msg}}, upsert=False)

def get_task_state(task_id):
    client = MongoClient()
    db = client.helix
    res = db.runningtask.find_one({'task_id' : task_id}, {'state' : 1, 'stage' : 1, 'stage_message' : 1, 'timestamp' : 1})
    return res

def new_workflow(workflow):
    client = MongoClient()
    db = client.helix
    document = {"workflow" : workflow, "count" : 0}
    return db.workflows.insert_one(document).inserted_id
    
def get_workflow_list():
    client = MongoClient()
    db = client.helix
    res = db.workflows.find({}, {'workflow':1})
    rlist = []
    for w in res:
        rlist.append(w['workflow'])
    return rlist
    

def new_version(task_id):
    client = MongoClient()
    db = client.helix
    tmp_document = db.runningtask.find_one({'task_id':task_id})
    print("debug")
    document = {}
    document["workflow"] = tmp_document["workflow"]
    document["task_id"] = tmp_document["task_id"]
    document["comment"] = tmp_document["comment"]
    document["timestamp"] = tmp_document["timestamp"]
    print(document)
    document["code"] = tmp_document["code"]
    db.versions.insert_one(document)
    db.workflows.update_one({'workflow': document['workflow']}, {'$inc':{'count':1}})
    print(db.workflows.find_one({'workflow': document['workflow']}))
