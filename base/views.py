from django import forms
from django.shortcuts import render , redirect
from django.http import HttpResponse
#we are importing the ListView class from django.views.generic
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Task
from django.views.generic.edit import CreateView, UpdateView, DeleteView , FormView
#reverse_lazy is used to redirect to a url after a successful form submission
from django.urls import reverse_lazy


from django.contrib.auth.views import LoginView , LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 
from django.contrib.auth.models import User
#LoginRequiredMixin is used to restrict access to a view to only authenticated users
from django.contrib.auth.mixins import LoginRequiredMixin


# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate




class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True#redirect to the home page if the user is already authenticated
    #if the user is not authenticated, the user will be redirected to the login page
    def get_success_url(self):#redirect to the tasks page after a successful login
        return reverse_lazy('tasks')




class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True#redirect to the home page if the user is already authenticated
    success_url=reverse_lazy('tasks')

    def form_valid(self, form):#if the form is valid, we are logging in the user
        user = form.save()#save the user to the database
        if user is not None:#if the user is created successfully
            login(self.request, user)#log in the user
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')#redirect to the tasks page if the user is already authenticated
        return super(RegisterPage, self).get(*args, **kwargs)
    


#we are enheriting from the ListView class(so we have all the functionalities of the ListView class)
class Tasks(LoginRequiredMixin,ListView):
    #by default the ListView class will look for a template with the name of the model in the app folder
    #so we have to specify the template name (task_list.html) in the template_name attribute
    model = Task
    context_object_name = 'tasks'#'tasks is used in a for loop in the template'
    
    #we are overriding the get_context_data method to add a new key-value pair to the context dictionary
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #we are filtering the tasks based on the user that created the task
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        #we are counting the number of tasks that are not done
        context['count'] = context['tasks'].exclude(status='done').count()
        SearchInput = self.request.GET.get('search') or ''
        if SearchInput:
            #filter the tasks based on the search input
            context['tasks'] = context['tasks'].filter(title__icontains=SearchInput)
            context['search'] = SearchInput
        return context         
    
  
class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'


class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields =['title','description','status','priority']
    success_url = reverse_lazy('tasks')#redirect to the tasks url after a successful form submission

    #we are overriding the form_valid method to add the user that created the task by default
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields = fields =['title','description','status','priority']
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')


