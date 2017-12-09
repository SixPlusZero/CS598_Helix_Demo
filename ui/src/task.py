from __future__ import absolute_import, unicode_literals
import os
from helix_ui.celery import training_job

def get_task_status(task_id):
    task = training_job.AsyncResult(task_id)
    status = task.status
    msg = ""
    stage = ""
    if status == 'SUCCESS':
        msg = "Task finished."
    elif status == 'FAILURE':
        msg = "Task failed."
    elif status == 'PROGRESS':
        msg = task.info['msg']
        stage = task.info['stage']
    return {'status' : status, 'message' : msg, 'stage' : stage}

def get_task_msg(task_id):
    task = training_job.AsyncResult(task_id)
    return task.get(on_message=on_raw_message, propagate=False)

def on_raw_message(body):
    print(body)