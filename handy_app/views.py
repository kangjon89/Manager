from django.shortcuts import render, HttpResponse, redirect
from log_app.models import User
from django.contrib import messages
from handy_app.models import *

def new_job(request):
    try:
        create_job = {
            "user": User.objects.get(id=request.session['user_id'])
        }
    except:
        return redirect('/')
    return render(request,'create_job.html', create_job)

def create(request):
    errors = Job.objects.trip_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/jobs/new')
    else:
        user = User.objects.get(id=request.session['user_id'])
        Job.objects.create(title=request.POST['title'], description=request.POST['description'], location=request.POST['location'], user=user)
        return redirect('/dashboard')

def edit(request, id):
    try:
        job = Job.objects.get(id=id)
        if request.session['user_id'] == job.user.id:
            edit_job = {
                "user": User.objects.get(id=request.session['user_id']),
                "job": Job.objects.get(id=id),
            }
            return render(request, 'edit_job.html', edit_job)
    except:
        return redirect('/dashboard')
    return redirect('/dashboard')

def update(request):
    errors = Job.objects.trip_validator(request.POST)

    if len(errors) > 0:
        job = Job.objects.get(id=request.POST['job'])
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(f'/jobs/edit/{job.id}')
    else:
        update_job = Job.objects.get(id=request.POST['job'])
        update_job.title = request.POST['title']
        update_job.description = request.POST['description']
        update_job.location = request.POST['location']
        update_job.save()
        return redirect('/dashboard')

def show(request, id):
    context = {
        "jobs": Job.objects.get(id=id),
        "user_logged_in": User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'show.html', context)

