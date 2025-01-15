from django import forms
from django import forms
from django.forms import ModelForm
from .models import Task
#1 Forma
class CreateNewTask(forms.Form):
    tittle = forms.CharField(label="",max_length=200, widget=forms.TextInput(attrs={'class':'form-control input','placeholder':'Title Task'}))
    description = forms.CharField(label="",widget=forms.Textarea(attrs={'class':'form-control input','placeholder':'Description'}), required=False)  # TextField es para modelos, usa CharField con Textarea
    important = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'input_important'}), required=False)  # default es un parámetro de modelos, aquí se usa required 

""" class CreateNewTask(forms.ModelForm):
    class Meta:
        model = Task  # Asocia el formulario con el modelo Task
        fields = ['tittle', 'description', 'important']  # Especifica los campos que quieres incluir
        widgets = {
            'tittle': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Title Task'}),
            'description': forms.Textarea(attrs={'class': 'input', 'placeholder': 'Description'}),
            'important': forms.CheckboxInput(attrs={'class': 'input_important'}),
        } """

