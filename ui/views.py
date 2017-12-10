# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib import messages
from helix_ui.celery import training_job
from ui.src import task
import ui.src.db as mdb
# Create your views here.
def index(request):
    context = {}
    return render(request, 'ui/index.html', context)

def editor(request):
    context = {}
    return render(request, 'ui/editor.html', context)

def train(request):
    mlcode = request.POST.get('mlcode')
    workflow = "CensusExample"
    comment = "empty comment"
    tid = training_job.apply_async(args=[workflow, mlcode, comment])
    context = {"task_id": tid.id}
    return render(request, 'ui/train.html', context)

def task_status(request):
    task_id = request.POST.get('task_id')
    print("Get request for task: %s" % (task_id))
    mres = mdb.get_task_state(task_id)
    res = {}
    res['state'] = mres['state']
    res['stage'] = mres['stage']
    res['stage_message'] = mres['stage_message']
    return JsonResponse(res)
