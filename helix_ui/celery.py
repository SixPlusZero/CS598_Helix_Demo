from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.contrib import messages
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
    cnt = 0
    for i in range(20):
        time.sleep(1)
        cnt += 5
        print(cnt)
        if (cnt == 100):
            training_job.update_state(state='SUCCESS', meta={'progress': cnt})
        else:
            training_job.update_state(state='PROGRESS', meta={'progress': cnt})

