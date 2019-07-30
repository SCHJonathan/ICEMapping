from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.db import connection
from django.views import generic
from .models import Tidychampaign, CommentDB
from .forms import UserInfoForm, CommentForm, recommandationForm
from .pyScript import distance as distance

#   Straightforward function.
def index(request):
    template = loader.get_template('datamanager/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


#   This is a very important function which might be changed several time in the future.
#   This function handle nearly all request for the detail page for a data record.
#
#   It handles: 1) listing all attribute for that record in Tidychampaign database
#               2) display all the comments from current logged-in user towards this data record.
#               3) display the form for user to write a new comment or provide the UI for user to manage their
#                  comments
#   Feel free to add additional features if you want.
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


#   This function is used to handled the request when user want to delete one of their comment.
#   I think this function is working very well. Feel free to change it if you find any bugs.
def deleteComment(request, geoid, context):
    username = request.user.username

    deleteQuery = """\
                DELETE FROM CommentDB
                WHERE GEOID = %s AND Username = '%s' AND Comment = '%s';
                """
    with connection.cursor() as cursor:
        cursor.execute(deleteQuery % (geoid, username, context))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


#   This function is for user provide their data (race, gender, location, etc.) to our database.
#   User provide their data via fill out a form. You can go to forms.py and take a look at UserInfoForm
#   function to have a better look.
#
#   The function here is just a first draft. Here are some potential improvements you can make:
#   1. The query for updating Tidychampaign database is very bad.
#           * It doesn't handle the case when user choose 'Prefer not to answer' option.
#           * Each user should only upload their data once. This query doesn't handle this case
#   2. Since we want each user can only update the query once, it would be nice if we can implement the
#      feature that after the user filled out the form once, it will display 'Thank you for your contribution!
#      You have filled out this form before!' (or stuff like this). We don't want a single user update the database
#      multiple times.
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

            age = form['age'].value()
            race = form['race'].value()
            gender = form['gender'].value()
            geoid = form['geoid'].value()

            place = get_object_or_404(Tidychampaign, pk=geoid)
            list = [age,race,gender];
            for item in list:
                if item != 'NA':

                    query = """\
                        UPDATE Tidychampaign
                        SET %s = %s + 1
                        WHERE GEOID = %s;
                        """
                    with connection.cursor() as cursor:
                         cursor.execute(query %(item, item, geoid))
            query = """\
                UPDATE Tidychampaign
                SET Population = Population + 1
                WHERE GEOID = %s;
                """
            with connection.cursor() as cursor:
                 cursor.execute(query %geoid)
        template = loader.get_template('datamanager/thanks.html')
        context = {
            'username' : username,
        }
    return HttpResponse(template.render(context, request))


#   This function is for listing all data record in our database. As you can see, I use the 'paginator' API for
#   this feature. If you are not familiar with this API, you can google it and see the documentation for reference.
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

#   This function is for handling the request for the recommandation
#   system.

#
#   This function is also incomplete.
#   1. I also don't handle the 'Prefer not to answer' edge cases.
#   2. As you can see from the query, it just sorts the table based on age,
#      race, gender and then join three table. Han Bro will use some
#      machine learning models to implement a better way to give user
#      recommandation. We need to integrate that.
def recommandation(request):
    if request.method == "GET":
        template = loader.get_template('datamanager/recommandation.html')
        form = recommandationForm()
        context = {
            'form' : form,
        }
        return HttpResponse(template.render(context, request))
    else:
        form = recommandationForm(request.POST)
        record_list = []
        if form.is_valid():
            age = form['age'].value()
            race = form['race'].value()
            gender = form['gender'].value()
            area = form['area'].value()
            # query = """\
            #     SELECT *
            #     FROM (SELECT *
            #           FROM Tidychampaign
            #           ORDER BY %s DESC LIMIT 10) AS AgeRank,
            #          (SELECT *
            #           FROM Tidychampaign
            #           ORDER BY %s DESC LIMIT 10) AS RaceRank,
            #          (SELECT *
            #           FROM Tidychampaign
            #           ORDER BY %s DESC LIMIT 10) AS GenderRank
            #     WHERE AgeRank.GEOID = RaceRank.GEOID
            #           AND
            #           GenderRank.GEOID = RaceRank.GEOID
            #     """
            data = distance.distance(area)
            # with connection.cursor() as cursor:
                # cursor.execute(query % (age, race, gender))
                # record_list = cursor.fetchall()
        template = loader.get_template('datamanager/recommandation.html')
        context = {
            'record_list' : data,
        }
        return HttpResponse(template.render(context, request))


#   I am using django built-in login-logout interface, which is legit enough so I think
#   currently there is no need to change this function.
def logout_request(request):
    logout(request)
    return redirect("datamanager:index")

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('datamanager:login')
    template_name = 'datamanager/signup.html'
