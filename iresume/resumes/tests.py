from django.test import TestCase
from .models import ResumeData, BLOG_QS
import json
from .views import UserFormView
from django.urls import reverse


# Create your tests here.
class ResumeDataModelTest(TestCase):
    def test_insert_required_field_pass(self):
        username = "test"
        name = "test"
        email = "test@test.com"
        resume_data = ResumeData(username=username,
                                 name=name,
                                 email=email)
        resume_data.save()
        self.assertEqual(resume_data.username, username)

    def test_auto_post_qs(self):
        username = "test"
        name = "test"
        email = "test@test.com"
        resume_data = ResumeData(username=username,
                                 name=name,
                                 email=email)
        resume_data.save()
        resume = ResumeData.objects.get(username=username)
        blogs = json.dumps(BLOG_QS)
        self.assertEqual(resume.post_qs, blogs)


class ViewsTest(TestCase):
    def setUp(self) -> None:
        self.username = 'test'
        self.data = {'username': self.username,
                     'password': 'test',
                     'email': 'test@test.com',
                     'name': 'test',
                     'contact': 2324}
        self.client.post(reverse('register'), self.data)

    def test_register_resume(self):
        resume_user = ResumeData.objects.get(username=self.username)
        self.assertEqual(resume_user.username, self.username)

    def test_skill_update(self):
        data = {'key_skill': 'python,django'}
        self.client.post(reverse('resumes:skills'), data)
        resume_user = ResumeData.objects.get(username=self.username)
        skills = json.dumps(data['key_skill'].split(','))
        self.assertEqual(resume_user.key_skills, skills)

    def test_empty_skill_update(self):
        data = {'key_skill': '  '}
        self.client.post(reverse('resumes:skills'), data)
        resume_user = ResumeData.objects.get(username=self.username)
        data['key_skills'] = '[]'
        self.assertEqual(resume_user.key_skills, data['key_skills'])

    def test_workexperience_update(self):
        data = {'start': '12/12/2001',
                'end': '12/12/2002',
                'company_name': 'test_company',
                'responsibility': 'test.test'}
        self.client.post(reverse('resumes:work'), data)
        data['responsibility'] = data['responsibility'].strip(' ').split('.')
        data = [data]
        resume_user = ResumeData.objects.get(username=self.username)
        self.assertEqual(json.loads(resume_user.work_experience),
                         data)

    def test_education_update(self):
        data = {'start': '12/12/2001',
                'end': '12/12/2002',
                'college_name': 'test_company',
                'university': 'test_university',
                'percentage': '20',
                'qualification': 'tester'}
        self.client.post(reverse('resumes:edu'), data)
        data = [data]
        resume_user = ResumeData.objects.get(username=self.username)
        self.assertEqual(json.loads(resume_user.education),
                         data)
