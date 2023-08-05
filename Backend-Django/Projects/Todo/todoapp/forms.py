from django import forms
from django.contrib.auth.models import User
from .models import Task

class TaskForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=True)
    class Meta:
        model = Task
        fields = ['user', 'title', 'description']
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            # 'complete': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
