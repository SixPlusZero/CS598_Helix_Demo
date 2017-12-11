# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib import messages
from helix_ui.celery import training_job
from ui.src import task
import json
import ui.src.db as mdb
import ui.src.util as util
# Create your views here.
def index(request):
    context = {}
    if request.GET.get('workflow') != None:
        wf = request.GET.get('workflow')
        vlist = mdb.get_version_list(wf)
        context['vlist'] = vlist
    return render(request, 'ui/index.html', context)

def editor(request):
    print("entering editor")
    context = {}
    if request.GET.get('tid_code') != None:
        d = mdb.get_code_by_task_id(request.GET.get('tid_code'))
        context['mlcode'] = d['code']
        context['workflow'] = d['workflow']
        if 'params' in d:
            context['params'] = d['params']
            context['paramcnt'] = d['paramcnt']
    if request.POST.get('newwfname') != None:
        context['workflow'] = request.POST.get('newwfname')
        context['mlcode'] = util.generate_template(request.POST.get('newwfname'))
    if request.POST.get('mlcode') != None:
        print("has code")
        mlcode = request.POST.get('mlcode')
        paramcnt = int(request.POST.get('paramcnt'))
        print "DEBUG GET PARAMCNT: ", paramcnt
        params = {}
        if (paramcnt != 0):
            for i in range(paramcnt):
                k = request.POST.get('key%d' % (i+1))
                v = request.POST.get('val%d' % (i+1))
                params[k] = v
        print "DEBUG GET PARAMS: ", params
        fillcode = util.code_fillup(mlcode)
        workflow = request.POST.get('workflow')
        comment = "Example comment"
        tid = training_job.apply_async(args=[workflow, mlcode, fillcode, params, comment])
        context["task_id"] = tid.id
        context["params"] = params
        context["paramcnt"] = paramcnt
        print(context["task_id"])
        context["mlcode"] = mlcode
    return render(request, 'ui/editor.html', context)

def task_status(request):
    task_id = request.POST.get('task_id')
    print("Get request for task: %s" % (task_id))
    mres = mdb.get_task_state(task_id)
    res = {}
    res['state'] = mres['state']
    res['stage'] = mres['stage']
    res['stage_message'] = mres['stage_message']
    return JsonResponse(res)

def workflow_list(request):
    res = json.dumps(mdb.get_workflow_list())
    print(res)
    return HttpResponse(res)
