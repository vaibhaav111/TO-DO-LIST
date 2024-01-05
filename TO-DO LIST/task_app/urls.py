
from django.contrib import admin
from . import views
from django.urls import path

app_name='tasks'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('signup/', views.signup.as_view(), name='signup'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('create/',views.task_create, name='task_create'),
    path('task_list/', views.task_list, name='task_list'),
    path(r'tasks/<int:pk>/delete/',views.task_delete,name='task_delete'),
    path(r'tasks/<int:pk>/update/', views.task_update, name='task_update'),
    ]

