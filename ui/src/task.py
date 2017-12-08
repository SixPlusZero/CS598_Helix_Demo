from __future__ import absolute_import, unicode_literals
import os
from helix_ui.celery import training_job

def get_task_status(task_id):
    task = training_job.AsyncResult(task_id)
    status = task.status
    progress = 0
    if status == u'SUCCESS':
        progress = 100
    elif status == u'FAILURE':
        progress = 0
    elif status == 'PROGRESS':
        progress = task.info['progress']
    return {'status': status, 'progress': progress}

def get_task_msg(task_id):
    task = training_job.AsyncResult(task_id)
    return task.get(on_message=on_raw_message, propagate=False)

def on_raw_message(body):
    print(body)