from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.contrib import messages
import ui.src.train as train
import ui.src.db as mdb
import time
import datetime

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helix_ui.settings')

app = Celery('helix_ui')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def training_job(self, workflow, code, comment):
    task_id = training_job.request.id
    mdb.new_task(task_id, workflow, datetime.datetime.utcnow(), comment, code)
    state = "RUNNING"
    stage = "SUBMIT"
    mdb.update_task_state(task_id, state, stage, 'Code submitted to server.')
    train.save_code(code)
    stage = "SAVECODE"
    mdb.update_task_state(task_id, state, stage, 'Code saved to helix engine.')
    train.compile_code()
    stage = "COMPILECODE"
    mdb.update_task_state(task_id, state, stage, 'Code compiled to helix engine.')
    mdb.get_task_state(task_id)
    train.run_code()
    stage = "RUNCODE"
    mdb.update_task_state(task_id, state, stage, 'Code executed.')
    state = "SUCCESS"
    stage = "FINISH"
    mdb.update_task_state(task_id, state, stage, 'Task completed.')
    mdb.get_task_state(task_id)
