from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^editor/$', views.editor, name='editor'),
    url(r'^task/$', views.task_status, name='task'),
    url(r'^wflist/$', views.workflow_list, name='wflist')
]