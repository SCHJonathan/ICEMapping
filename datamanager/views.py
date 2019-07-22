from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.db import connection
from .models import Tidychampaign

def index(request):
    all_list = Tidychampaign.objects.all()
    template = loader.get_template('datamanager/index.html')
    context = {
        'all_list': all_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, geoid):
    place = get_object_or_404(Tidychampaign, pk=geoid)
    return render(request, 'datamanager/detail.html', {'place': place})

def results(request, geoid):
    place = get_object_or_404(Tidychampaign, pk=geoid)
    return render(request, 'datamanager/results.html', {'place': place})
    