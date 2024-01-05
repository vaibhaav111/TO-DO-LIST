# Create your views here.
from django.urls import reverse
from .models import Task
from .forms import TaskForm
from django.contrib.auth import logout
from django.views.generic import CreateView
from .forms import SignUpForm
from .models import User
from django.core.cache import cache
from django.core.mail import send_mail
import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect


# Create your views here.

def home(request):
    return render(request, 'Tasks/home.html')

# def register(request):
#     return render(request, 'Tasks/register.html')

class signup(CreateView): # # used to handle the submission of form
    model = User #DB
    form_class = SignUpForm  # USER
    template_name= 'Tasks/student_register.html'

    def form_valid(self, form):
        user = form.data_save()
        login(self.request, user)
        return redirect('tasks:login_user')



def login_user(request):
    # POST refers to an HTTP method. HTTP (Hypertext Transfer Protocol) is the protocol used for
    # transmitting data on the internet. There are several HTTP methods,
    # and two common ones are GET and POST.
    form = AuthenticationForm()  # where users can write their username and password.
    if request.method == 'POST': #The code first checks if the user has submitted the login form
        form = AuthenticationForm(data=request.POST) #It creates a login form using the submitted data and checks if it's valid
        if form.is_valid(): #If the form is valid, it extracts the username and password entered by the user.
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)#It tries to authenticate the user using the provided username and password.


            if user is not None:
                login(request, user)  # If authentication is successful, it logs in the user using login(request, user).
                return redirect((reverse('tasks:task_create')))#After successful login, it redirects the user to the task creation page.
            else:
                messages.error(request, "Invalid username or password")#if there are any errors (invalid form, authentication failure), it shows an appropriate error message.
        else:
            messages.error(request, "Invalid username or password")#Finally, it renders the login page, either with a fresh form or with error messages.


    # form= AuthenticationForm()#where users can write their username and password.
    return render(request, 'Tasks/login.html', {'form':form})


def logout_user(request):
    logout(request)
    return redirect('/tasks/home')


#create
def task_create(request):   # to add new task
    # print(request) #to see what data is being sent with the request. in console log
    if request.method == "POST": #This is like asking, "Did someone fill out a form and submit it to us?"
        form=TaskForm(request.POST) #it creates a form (TaskForm) with the data from the submitted form.
        if form.is_valid():#Checks if the submitted form is valid.
            task = form.save(commit=False) #If the form is valid, it creates a new task with the form data, assigns the user who submitted the form, and saves it to the database.
            task.user = request.user  # Set the user field to the currently logged-in user
            task.save()
            return redirect('http://127.0.0.1:8000/tasks/task_list/') #After creating the task, it sends the user to the task list page.
    else:
        form=TaskForm() #If it's not a form submission, meaning the user is just loading the page, it creates an empty form
    return render(request, "Tasks/task_form.html",{'form':form,}) #It renders the HTML page for creating a task, providing the form to the template.


def task_list(request):
    today = datetime.date.today()#This line gets the current date.
    tasks = Task.objects.filter(user=request.user)#This line retrieves tasks associated with the currently logged-in user.
    from_email = "harsithsanthoshkumar@gmail.com"  # Update with your email
    recipient_list =[request.user.email]# sender's email address and the recipient's email address(current user)
    tasks_for_current_date = tasks.filter(t_date=today)#This line filters tasks to find those that have the same date as today.

    if tasks_for_current_date.exists(): #This line checks if there are tasks scheduled for the current date.
        for task in tasks:
          if task.t_date == today: #For each task, it checks if the task's date is the same as today.
            subject = "Task Reminder"
            message = f"Reminder: You have a remainder today - {task.name}"   # formatted text
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)  #fail_silently = "if there's a problem, I want to know about it!"
            # Set a flag to indicate that an email has been sent today
            cache.set('email_sent_today', True, 60 * 60 * 24)
    return render(request, "l1.html", {'tasks': tasks})


#A cache is a place to temporarily store data so that it can be quickly retrieved later.
#.set(): This is a method/function used to set a value in the cache.

# #delete
def task_delete(request,pk):
    task_obj=Task.objects.get(pk=pk)
    task_obj.delete()
    return redirect(reverse("tasks:task_list"))



def task_update(request,pk):
    task=Task.objects.get(pk=pk) #This line retrieves the task that needs to be updated. It uses the primary key (pk) to identify the specific task.
    if request.method == "POST": #It checks if the user has submitted a form (POST request). This is typically the case when a user fills out a form on a webpage.
        form=TaskForm(instance=task,data=request.POST) #f it's a form submission, it creates a form (TaskForm) with the data from the submitted form. The instance=task part pre-fills the form with the existing data of the task being updated.
        if form.is_valid():
            form.save()
            return redirect('tasks:task_list')

    else:
        form=TaskForm(instance=task) #If it's not a form submission (e.g., the user is just viewing the page), it creates a form instance with the existing task data.
    return render(request, "update.html", {"form":form, "object":task})
