from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.db import connection
from django.views import generic
from .models import Tidychampaign, UserInfo
from .forms import UserInfoForm

def index(request):
    template = loader.get_template('datamanager/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def detail(request, geoid):
    place = get_object_or_404(Tidychampaign, pk=geoid)
    return render(request, 'datamanager/detail.html', {'place': place})

def results(request, geoid):
    place = get_object_or_404(Tidychampaign, pk=geoid)
    return render(request, 'datamanager/results.html', {'place': place})

def logout_request(request):
    logout(request)
    return redirect("datamanager:index")

def newdata(request, username):
    if request.method == "GET":
        template = loader.get_template('datamanager/newdata.html')
        form = UserInfoForm()
        context = {
            'username' : username,
            'form' : form,
        }
    else:
        form = UserInfoForm(request.POST)
        if form.is_valid():
            username = form['username'].value()
            email = form['email'].value()
            age = form['age'].value()
            race = form['race'].value()
            gender = form['gender'].value()
            geoid = form['geoid'].value()

            query = """\
                UPDATE Tidychampaign
                SET %s = %s + 1, %s = %s + 1, %s = %s + 1
                WHERE GEOID = %s;
                """
            with connection.cursor() as cursor:
                 cursor.execute(query % (age, age, race, race, gender, gender, geoid))

        template = loader.get_template('datamanager/thanks.html')
        context = {
            'username' : username,
        }
    return HttpResponse(template.render(context, request))

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('datamanager/login')
    template_name = 'datamanager/signup.html'