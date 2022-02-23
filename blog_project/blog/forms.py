from django import forms
from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from blog.models import (Post)
from datetimewidget.widgets import DateTimeWidget


class RegistrationForm(UserCreationForm):#Form validasyon sağlıyor.
    email = forms.EmailField(label='Email', max_length=100)
    class Meta:
        model=User
        fields=("email","username","password1","password2") 


class AccountAuthenticationForm(forms.ModelForm):
    password=forms.CharField(label='Password',widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=('username','password')        
    '''def clean(self):
        if(self.is_valid()):
            username=self.cleaned_data['username']
            password=self.cleaned_data['password']    
            if not authenticate(username=username,password=password):
                raise forms.ValidationError("Invalid login.")''' #Bunu burada yazman mantıksız formlarda datayla alakalı kontrol yapılmaz.


class AddPostForm(forms.ModelForm):
    publish = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'id':'dateTimePicker'
        })
    )
    image= forms.ImageField(required=False)
    url=forms.URLField(required=False)
    email=forms.EmailField(required=False)
    title=forms.CharField(widget=forms.TextInput(attrs={'id':'title_blank'}))
    slug=forms.SlugField(required=False,disabled=True,widget=forms.TextInput(attrs={'id':'slug_blank'}))
    class Meta:
        model=Post
        fields=("title",'slug','content','body','publish','status','image','url','email')
        