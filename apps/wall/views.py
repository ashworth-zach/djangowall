from django.shortcuts import render, redirect
import bcrypt
from .models import *
from django.contrib import messages
def index(request):
    return render(request, 'wall/index.html')
def add(request):
    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = User.objects.basic_validator(request.POST)
        # check if the errors object has anything in it
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        # if the errors object is empty, that means there were no errors!
        # retrieve the user to be updated, make the changes, and save
        request.session['email']=request.POST['email']
        user = User.objects.create()
        user.firstname = request.POST['firstname']
        user.lastname = request.POST['lastname']
        user.email = request.POST['email']
        user.pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user.save()
        messages.success(request, "User successfully added")
        # redirect to a success route
        return redirect('/thewall')
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    request.session['email']=request.POST['email']
    return redirect('/thewall')
def show(request):
    context={
        'user':User.objects.all().values().get(email=request.session['email']),
        'messages':Message.objects.all().values(),
        'comments':Comment.objects.all().values()
    }
    return render(request, 'wall/thewall.html', context)
