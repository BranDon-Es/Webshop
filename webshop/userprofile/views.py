from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.text import slugify

from .models import Userprofile

from storefront.forms import ServiceForm
from storefront.models import Service, Category


def vendor_detail(request, pk):
    user = User.objects.get(pk=pk)
    services = user.services.filter(status=Service.ACTIVE)

    return render(request, 'userprofile/vendor_detail.html', {
        'user': user,
        'services': services
    })


@login_required
def my_store(request):
    services = request.user.services.exclude(status=Service.DELETED)

    return render(request, 'userprofile/my_store.html', {
        'services': services
    })


@login_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)

        if form.is_valid():
            title = request.POST.get('title')

            service = form.save(commit=False)
            service.user = request.user
            service.slug = slugify(title)
            service.save()

            messages.success(request, 'The service was added.')

            return redirect('my_store')

    else:
        form = ServiceForm()

    return render(request, 'userprofile/add_service.html', {
        'title': 'Add service',
        'form': form
    })


@login_required
def edit_service(request, pk):
    service = Service.objects.filter(user=request.user).get(pk=pk)

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)

        if form.is_valid():
            form.save()

            messages.success(request, 'The changes have been made.')

            return redirect('my_store')
    else:
        form = ServiceForm(instance=service)

    return render(request, 'userprofile/add_service.html', {
        'title': 'Edit service',
        'service': service,
        'form': form
    })


def delete_service(request, pk):
    service = Service.objects.filter(user=request.user).get(pk=pk)
    service.status = Service.DELETED
    service.save()

    messages.success(request, 'The service was deleted.')

    return redirect('my_store')

@login_required
def myaccount(request):
    return render(request, 'userprofile/myaccount.html')


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            userprofile = Userprofile.objects.create(user=user)

            return redirect('frontpage')

    else:
        form = UserCreationForm()

    return render(request, 'userprofile/signup.html', {
        'form': form
    })
