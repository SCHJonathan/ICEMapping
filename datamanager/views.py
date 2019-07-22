from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.db import connection
from .models import Tidychampaign, User
from .forms import userRegistration

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
    
def login(request):
    form = userRegistration(request.POST)
    if form.is_valid():
        username = form['username'].value()
        passward = form['password'].value()
        entry = User.objects.get(pk=username)
        if entry:
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            insert_query = 'INSERT INTO User (Username,Password) VALUES (%s, %s);'
            with connection.cursor() as cursor:
                cursor.execute(insert_query, (username, passward))
            return HttpResponseRedirect(reverse('polls:index'))
