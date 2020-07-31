from rest_framework import serializers
from .models import ResumeData


class ResumeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeData
        fields = ['name', 'job_title', 'work_experience', 'education', 'email', 'contact', 'personal_profile',
                  'key_skills','post_qs','post_as']


