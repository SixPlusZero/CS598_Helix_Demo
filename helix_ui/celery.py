from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.contrib import messages
import ui.src.train as train
import time

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
def training_job(self, code):
    stage = "submit"
    training_job.update_state(state='PROGRESS', meta={'stage':stage, 'msg': 'Code submitted to server.'})
    wf = train.save_code(code)
    print("workflow name is %s" % (wf))
    stage = "savecode"
    training_job.update_state(state='PROGRESS', meta={'stage':stage, 'msg': 'Code saved to helix engine.'})
    train.compile_code()
    stage = "compilecode"
    training_job.update_state(state='PROGRESS', meta={'stage':stage, 'msg': 'Code compiled to helix engine.'})
    train.run_code()
    stage = "runcode"
    training_job.update_state(state='PROGRESS', meta={'stage':stage, 'msg': 'Code executed.'})

    training_job.update_state(state='SUCCESS', meta={'stage':stage, 'msg': 'Task completed.'})

