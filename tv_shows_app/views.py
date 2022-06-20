from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Show
from datetime import datetime
from django.contrib import messages


def index(request):
    return redirect('/shows')

def new_show(request):
    return render(request,'create_newshow.html')

def create_new_show(request):
    if request.method=="POST":
        errors = Show.objects.basic_validation(request.POST)
        if len(errors)>0:
            for key, value  in errors.items():
                messages.error(request, value)
        else:
            title=request.POST.get('title')
            nw=request.POST.get('nw')
            date=request.POST.get('date')
            desc=request.POST.get('desc')
            show1=Show.objects.create(title=title,network=nw,date=date,desc=desc)
            return redirect(reverse('view_show',args=(show1.id,)))
    return redirect(reverse('new_show'))

def view_show(request,id):
    show=Show.objects.get(id=id)
    context={
        'show':show,
    }
    return render(request,'view_show.html',context)

def list_shows(request):
    context={
        'shows':Show.objects.all()
    }
    return render(request,'shows_list.html',context)

def edit_show(request,id):
    show=Show.objects.get(id=id)
    context={
        'show':show,
        
    }
    return render(request,'edit_show.html',context)

def update_show(request,id):
    
    if request.method=="POST":
        errors = Show.objects.basic_validation(request.POST)
        show=Show.objects.get(id=id)
        if len(errors)>0:
            for key, value  in errors.items():
                messages.error(request, value)
            return redirect(reverse('edit_show',args=(show.id,)))
        else:
            show.title=request.POST.get('title')
            show.network=request.POST.get('nw')
            
            #if there is date we assign it, if there is none pass, 
            #we need this condtion because it gives error if input date is empty
            if request.POST['date']:
                show.date=request.POST.get('date')
            show.desc=request.POST.get('desc')
            show.save()
    return redirect(reverse('view_show',args=(show.id,)))

def destroy_show(request,id):
    Show.objects.get(id=id).delete()
    return redirect('/shows')