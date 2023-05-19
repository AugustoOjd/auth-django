from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        # estilizar estilos desde form python
        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'form-control'})
        # }