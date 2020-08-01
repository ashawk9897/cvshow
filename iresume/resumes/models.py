from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django import forms
from django.contrib.postgres.fields import JSONField
import json

# Create your models here.
def script_injection(value):
    if value.find('<script>') != -1:
        raise ValidationError(_('Script injection in %(value)s'),
                              params={'value': value})


BLOG_QS = ["My journey at job", "My expectations from final year", "How my site is structured and django",
           "How I used TDD to develop my app"]
BLOG_AS=['Not answered' for _ in BLOG_QS]


class Experience(models.Model):
    start = models.CharField(max_length=100)
    end = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=400)
    responsibility = ArrayField(models.TextField(null=True, blank=True), blank=True)

    class Meta:
        abstract = True


class DateInput(forms.DateInput):
    input_type = 'date'


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['start', 'end', 'company_name', 'responsibility']
        widgets = {
            'start': DateInput(attrs={'class': 'form-control'}),
            'end': DateInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'placeholder': 'Company Name', 'class': 'form-control'}),
            'responsibility': forms.Textarea(attrs={'placeholder': 'Responsibility', 'class': 'form-control'}),
        }


class Education(models.Model):
    id = models.AutoField(primary_key=True)
    start = models.CharField(max_length=100)
    end = models.CharField(max_length=100, blank=True, null=True)
    college_name = models.CharField(max_length=900)
    university = models.CharField(max_length=900)
    qualification = models.CharField(max_length=400)
    percentage = models.FloatField(max_length=3)

    class Meta:
        abstract = True


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['start', 'end', 'college_name', 'university', 'qualification', 'percentage']
        widgets = {
            'start': DateInput(attrs={'class': 'form-control'}),
            'end': DateInput(attrs={'class': 'form-control'}),
            'college_name': forms.TextInput(attrs={'placeholder': 'College Name', 'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'placeholder': 'Qualification', 'class': 'form-control'}),
            'percentage': forms.NumberInput(attrs={'placeholder': 'Percentage %', 'class': 'form-control'}),
            'university': forms.TextInput(attrs={'placeholder': 'University', 'class': 'form-control'}),
        }


class ResumeData(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    job_title = models.TextField(null=True)
    email = models.CharField(max_length=200)
    contact = models.BigIntegerField(max_length=12, null=True)
    personal_profile = models.TextField(null=True)
    work_experience = models.TextField(null=True)
    key_skills = models.TextField(null=True)
    education = models.TextField(null=True)
    post_qs = models.TextField(default=json.dumps(BLOG_QS))
    post_as = models.TextField(default=json.dumps(BLOG_AS))
    # objects = models.DjongoManager()
