from __future__ import absolute_import, unicode_literals
import os
from helix_ui.celery import training_job

def get_task_status(task_id):
    task = training_job.AsyncResult(task_id)
    status = task.status
    msg = ""
    print(task)
    print(task.info)
    if status == 'SUCCESS':
        if task.info != None: msg = task.info['msg']
    elif status == 'FAILURE':
        if task.info != None: msg = task.info['msg']
    elif status == 'PROGRESS':
        if task.info != None: msg = task.info['msg']
    return {'status': status, 'message' : msg}

def get_task_msg(task_id):
    task = training_job.AsyncResult(task_id)
    return task.get(on_message=on_raw_message, propagate=False)

def on_raw_message(body):
    print(body)