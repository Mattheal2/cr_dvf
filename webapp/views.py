from django.shortcuts import render
from django.http import HttpResponse
from django.apps import apps
from django.template import loader
from .data import graphes

def index(request):
  template = loader.get_template('index.html')
  data = apps.get_app_config('webapp').data
  
  context = {
    'graph1': graphes.get_graph1(data),
    'graph2': graphes.get_graph2(data),
    'graph3': graphes.get_graph3(data),
  }
  
  return HttpResponse(template.render(context=context))