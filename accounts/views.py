from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Customer
from .forms import CreateUserForm, CustomerForm
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib import messages
# from django.contrib.auth.models import User


def accountsHome(request):
    context = {}
    return render(request, 'accounts/AccountsHome.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):

    context = {}
    return render(request, 'accounts/User.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['procustomer'])
# def prouserPage(request):

#     context = {}
#     return render(request, 'accounts/PROUser.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def adminPage(request):

    context = {}
    return render(request, 'accounts/Admin.html', context)


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()  # from
    #ajax
    # username = request.GET.get('username', None)
    # is_present = User.objects.filter(username__iexact=username).exists()
    # print(is_present)


    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
            )

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/Register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('accountshome')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/Login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/AccountSettings.html', context)
