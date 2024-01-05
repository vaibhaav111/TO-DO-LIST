from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django import forms
from task_app.models import registation,User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta): #META IS A INHERIHETED CLASS
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'phone_number', 'email')

    @transaction.atomic
    def data_save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.is_coustomer= True
        user.save()
        user1 = registation.objects.create(user=user,
        email=self.cleaned_data.get('email'),
        phone_number=self.cleaned_data.get('phone_number'))
        user1.save()
        return user

class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields= ['name', 't_date', 'status']
        widgets = {
            't_date': forms.DateInput(attrs={'type': 'date'}),
        }



