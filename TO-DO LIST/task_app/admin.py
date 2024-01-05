from django.contrib import admin

# Register your models here.


from django.contrib import admin
from task_app.models import registation,Task

# Register your models here.
# class Task_Admin(admin.ModelAdmin):
#     list_display = ('name','t_date','status')
# admin.site.register(Task, Task_Admin)

admin.site.register(Task)
admin.site.register(registation)