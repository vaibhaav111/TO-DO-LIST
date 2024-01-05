from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
# Create your models here.
class User(AbstractUser): #

    is_coustomer = models.BooleanField(default=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)

class registation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=10)
    # email_id = models.EmailField()
#
class Status(models.TextChoices):
    UNSTARTED='u',"Not yet started"
    ONGOING='o',"Ongoing"
    Finished='f',"Finished"

class Task(models.Model):
    task_id=models.AutoField(max_length=3,primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(verbose_name="Task name", max_length=65, unique=False)
    t_date=models.DateField(verbose_name="Date")
    status=models.CharField(verbose_name="Task status", max_length=1, choices=Status.choices)

    def __str__(self):
        return self.name
