from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .forms import RegisterUserForm, UpdateUserProfile
from .models import UserAccount
from books.models import Borrow


from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string



def registerUser(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterUserForm()

    return render(request, 'users/user_form.html', {'form':form, 'type':'Register'})


def loginUser(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        if form.is_valid():
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"'{username}' logged in successfully")
                return redirect('home')
            else:
                messages.error(request, f"'{username}' user not found !!!")
        else:
            try:
                User.objects.get(username=username)
                messages.error(request, "Your Password is incorrect !!!")
            except:
                messages.error(request, f"'{username}' user not found !!!")
    else:
        form = AuthenticationForm()           
    return render(request, 'users/user_form.html',{'form':form, 'type':'Login'})


@login_required(login_url='login')
def updateProfileUser(request):
    if request.method == "POST":
        form = UpdateUserProfile(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account updated successfully for {username}!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UpdateUserProfile(instance=request.user)
    return render(request, 'users/user_form.html', {'form':form, 'type':'Update Profile'})


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    messages.info(request, 'Logout successfull !!!')
    return redirect('login')

@login_required(login_url='login')
def deposit(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        amount = int(amount)
        if amount < 100:
            messages.error(request, 'You have to deposit at least 100 BDT !!!')
        elif amount > 10000:
            messages.error(request, "You can't deposit more than 10000 BDT  for a single time !!!")
        elif amount:
            user_account = UserAccount.objects.get(user=request.user)
            user_account.balance += amount
            user_account.save()
            messages.success(request, 'Deposit successful!')
            #email
            email_message  = render_to_string('users/deposit_email.html', {
                'user' : request.user,
                'amount' : amount,
            })
            send_email = EmailMultiAlternatives('Deposit To Library', '', to=[request.user.email])
            send_email.attach_alternative(email_message , 'text/html')
            send_email.send()
            
            return redirect('deposit') 
    
    return render(request, 'users/deposit_form.html')

@login_required(login_url='login')
def profileUser(request):
    user = request.user
    borrows = Borrow.objects.filter(user=user)
    return render(request, 'users/profile.html', {'borrows': borrows})