from django.contrib.auth.models import User
from django import forms
from .models import ResumeData


class BasicForm(forms.ModelForm):
    class Meta:
        model = ResumeData
        fields = ['job_title', 'email', 'contact', 'personal_profile', 'key_skills']
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'contact': forms.NumberInput(attrs={'placeholder': 'Contact Number', 'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'placeholder': 'Job Title', 'class': 'form-control'}),
            'personal_profile': forms.Textarea(attrs={'placeholder': 'Personal Profile', 'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        super(BasicForm, self).__init__(*args, **kwargs)
        self.fields['job_title'].required = False
        self.fields['contact'].required = False
        self.fields['personal_profile'].required = False
        self.fields['key_skills'].required = False


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput({'placeholder': 'Password'}))
    contact = forms.IntegerField(widget=forms.NumberInput({'placeholder': 'Phone Number'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'contact', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),

        }


class UserLogin(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class ForgotPassword(forms.Form):
    email = forms.EmailInput(attrs={'placeholder': 'Email'})
