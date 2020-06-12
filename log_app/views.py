from django.shortcuts import render, HttpResponseRedirect ,HttpResponse, redirect
from log_app.models import *
from handy_app.models import Job
from django.contrib import messages
import bcrypt

# homepage 
def index(request):
    return render(request, 'log_in.html')

#registeration portion
def registration(request):
    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        #creates new User
        needed_id = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
        request.session['user_id'] = needed_id.id
        request.session['r_or_l'] = "registered!"
        return redirect('/dashboard')

#login portion
def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]

        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            request.session['r_or_l'] = "logged in!"
            return redirect('/dashboard')

    return redirect('/')

def dashboard(request):
    try:
        context = {
            "user": User.objects.get(id=request.session['user_id']),
            "jobs": Job.objects.all(),
        }
    except:
        return redirect('/')
    return render(request, 'dashboard.html', context)

def success(request):
    context = {
        "user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'success.html', context)

def log_out(request):
    request.session.flush()
    return redirect('/')

def delete(request, id):
    try:
        job = Job.objects.get(id=id)
        if request.session['user_id'] == job.user.id:
            delete_trip = Job.objects.get(id=id)
            delete_trip.delete()
    except:
        redirect('/dashboard')
    return redirect('/dashboard')
