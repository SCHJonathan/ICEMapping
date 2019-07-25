from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.db import connection
from django.views import generic
from .models import Tidychampaign, UserInfo, CommentDB
from .forms import UserInfoForm, CommentForm

def index(request):
    template = loader.get_template('datamanager/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def detail(request, geoid):
    if request.method == "GET":
        list_comment = []
        username = request.user.username
        template = loader.get_template('datamanager/detail.html')
        place = get_object_or_404(Tidychampaign, pk=geoid)

        commentQuery = """\
                   SELECT * 
                   FROM CommentDB 
                   WHERE GEOID = %s AND Username = '%s';
                   """
        with connection.cursor() as cursor:
                cursor.execute(commentQuery % (geoid, username))
                list_comment = cursor.fetchall()

        form = CommentForm()
        context = {
            'record' : place,
            'form' : form,
            'comments' : list_comment,
        }
        return HttpResponse(template.render(context, request))

    else:
        form = CommentForm(request.POST)
        emptyFrom = CommentForm()
        template = loader.get_template('datamanager/detail.html')
        place = get_object_or_404(Tidychampaign, pk=geoid)
        rate = 0
        list_comment = []

        if form.is_valid():
            username = request.user.username
            rate = form['rate'].value()
            comment = form['comment'].value()

            commentQuery = """\
                       SELECT * 
                       FROM CommentDB 
                       WHERE GEOID = %s AND Username = '%s';
                       """

            insertQuery = """\
                        INSERT INTO CommentDB(GEOID, Username, Rate, Comment)
                        VALUES (%s, '%s', %s, '%s');
                        """
            with connection.cursor() as cursor:
                cursor.execute(insertQuery % (geoid, username, rate, comment))
                cursor.execute(commentQuery % (geoid, username))
                list_comment = cursor.fetchall()
            

        context = {
            'record' : place,
            'form' : emptyFrom,
            'comments' : list_comment,
        }
        return HttpResponse(template.render(context, request))

def deleteComment(request, geoid, context):
    username = request.user.username

    deleteQuery = """\
                DELETE FROM CommentDB
                WHERE GEOID = %s AND Username = '%s' AND Comment = '%s';
                """
    with connection.cursor() as cursor:
        cursor.execute(deleteQuery % (geoid, username, context))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

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

def datalist(request):
    username = request.user.username
    records = Tidychampaign.objects.order_by("geoid")
    paginator = Paginator(records, 10)
    page = request.GET.get('page')
    try:
        show_records = paginator.page(page)
    except PageNotAnInteger:
        show_records = paginator.page(1)
    except EmptyPage:
        show_records = paginator.page(paginator.num_pages)
    template = loader.get_template('datamanager/datalist.html')
    context = {
        'records' : show_records,
    }
    return HttpResponse(template.render(context, request))

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('datamanager/login')
    template_name = 'datamanager/signup.html'