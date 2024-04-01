from django.template import loader
from django.shortcuts import render

def app_page(request):
  template = 'index.html'
  return render(request, template)