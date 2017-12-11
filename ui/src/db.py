import os
import sys
import time
import datetime
from pymongo import MongoClient

def new_task(task_id, workflow, timestamp, comment, params, code):
    document = {
        "task_id" : task_id,
        "workflow" : workflow,
        "timestamp" : timestamp,
        "comment" : comment,
        "code" : code,
        "params" : params
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

def get_version_list(workflow):
    client = MongoClient()
    db = client.helix
    res = db.versions.find({"workflow" : workflow}, {'workflow':1, 'timestamp':1, 'comment':1, 'accuracy':1, 'runtime':1, 'code':1, 'comment':1, 'task_id':1, 'params':1})
    vlist = []
    for w in res:
        p = {}
        p['workflow'] = w['workflow']
        p['timestamp'] = (w['timestamp'] - datetime.datetime(1970,1,1)).total_seconds()
        p['comment'] = w['comment']
        p['runtime'] = w['runtime']
        p['code'] = w['code']
        p['comment'] = w['comment']
        p['task_id'] = w['task_id']
        p['params'] = w['params']
        print p['params']
        if 'accuracy' in w:
            p['accuracy'] = w['accuracy']
        else:
            p['accuracy'] = -1.0
        vlist.append(p)
    return vlist
    

def new_version(task_id):
    client = MongoClient()
    db = client.helix
    tmp_document = db.runningtask.find_one({'task_id':task_id})
    document = {}
    document["workflow"] = tmp_document["workflow"]
    document["task_id"] = tmp_document["task_id"]
    document["comment"] = tmp_document["comment"]
    document["timestamp"] = tmp_document["timestamp"]
    document["code"] = tmp_document["code"]
    document["params"] = tmp_document["params"]
    if (db.workflows.count({"workflow":document["workflow"]}) == 0):
        new_workflow(document["workflow"])
    db.versions.insert_one(document)
    db.workflows.update_one({'workflow': document['workflow']}, {'$inc':{'count':1}})
    #print(db.workflows.find_one({'workflow': document['workflow']}))
    #print(db.workflows.count({'workflow': document['workflow']}))
    
def update_version(workflow, task_id, params):
    client = MongoClient()
    db = client.helix
    db.versions.update_one({'task_id' : task_id}, {'$set' : params}, upsert=False)

def get_code_by_task_id(task_id):
    client = MongoClient()
    db = client.helix
    w = db.versions.find_one({'task_id' : task_id})
    ans = {'workflow':w['workflow']}
    if 'code' in w:
        ans['code'] = w['code']
    if 'params' in w:
        ans['params'] = w['params']
        ans['paramcnt'] = len(w['params'])
    return ans
    
    