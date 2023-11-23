from django import forms

from ToDoapp.models import Task


class Taskform(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','complete']