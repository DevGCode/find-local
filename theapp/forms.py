from django.forms import ModelForm
from django import forms
from .models import *



class EmailSignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "type": "email",
        "name": "email",
        "id": "email",
        "placeholder": "Type your email address",
    }), label="")

    class Meta:
        model = Signup
        fields = ('email', )


class ContactForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = '__all__'
        widgets={
                   "name":forms.TextInput(attrs={'class': "form-control form-control-sm"}),
                   "phone":forms.TextInput(attrs={'class': "form-control form-control-sm"}),
                   "email":forms.TextInput(attrs={'class': "form-control form-control-sm"}),
                   "address":forms.TextInput(attrs={'class': "form-control form-control-sm"}),
                }



class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)
    catid = forms.IntegerField()
