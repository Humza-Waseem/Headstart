from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
##http resonse
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import MyUserCreationForm
from django.contrib import messages



# @login_required(login_url="UserLogin")
def homepage(request):
   return render(request, 'Auth/homepage.html')
    # return HttpResponse("Hello, world. You're at the polls index.")


def GuestHomePage(request):
    return render(request, 'Auth/GuestHomePage.html')

@login_required(login_url="UserLogin")
def UserHomePage(request):
    return render(request, 'Auth/UserHomePage.html')






def registerUser(request):
    form = MyUserCreationForm()  # Initialize the form

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)  # Initialize form with POST data
        if form.is_valid():
            # Save the user (commit=False means we can modify before saving)
            user = form.save()  # Save the user to the database

            # Log the user in automatically after registration
            # login(request, user)
            messages.success(request, 'Account was created for ' + user.username)
            return render(request,'UserLogin',{'form':form,'page':'login'})  # Redirect to homepage after successful registration
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'Auth/UserLogin.html', {'form': form, 'page': 'register'})






class UserLogin(LoginView):
    template_name = 'Auth/UserLogin.html'
    redirect_authenticated_user = True  # Redirects the user to the home page if the user is already logged in
    
    def get_success_url(self):
        messages.success(self.request, 'Logged In Successfully! Welcome Back '+ self.request.user.username)
        return reverse_lazy('homepage')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'login'  # Add 'login' to the context
        return context
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid login credentials. Please try again.')
        return super().form_invalid(form)
    
def UserLogout(request):    
    logout(request)   
    return redirect('homepage')   
