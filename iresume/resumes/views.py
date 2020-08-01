from django.shortcuts import render, redirect
from .models import ResumeData, EducationForm, ExperienceForm
from .forms import BasicForm, UserForm, UserLogin
from .serializers import ResumeDataSerializer
from django.db import connection
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import json


def cleandata(data):
    serialized = ResumeDataSerializer(data)
    work_experience = []
    education = []
    basicdata = {}
    key_skills = []
    for d in serialized:
        # print(d.name)
        # print(d.value)
        # print(type(d.value))
        if d.name == 'work_experience':
            work_experience = json.loads(d.value)
        elif d.name == 'key_skills':
            key_skills = json.loads(d.value)
        elif d.name == 'education':
            education = json.loads(d.value)
        elif d.name == 'post_qs':
            print(d.value)
            post_qs = json.loads(d.value)
        elif d.name == 'post_as':
            post_as = json.loads(d.value)
        else:
            basicdata[d.name] = d.value
    basicdata.update({'work_experience': work_experience[::-1],
                      'education': education[::-1],
                      'key_skills': key_skills,
                      'posts': list(zip(post_qs, post_as))})
    return basicdata


# Create your views here.
def home(request, username):
    if request.method == 'GET':
        print(username)
        data = ResumeData.objects.get(username=username)
        print(data)
        basicdata = cleandata(data)
        return render(request, 'index.html', context=basicdata)


@login_required(login_url='login')
def editmode(request):
    current_user = request.user
    if request.method == 'POST':
        data = ResumeData.objects.get(username=current_user)
        job_title = data.job_title if not request.POST.get('job_title') else request.POST.get('job_title')
        email = data.email if not request.POST.get('email') else request.POST.get('email')
        contact = data.contact if not request.POST.get('contact') else request.POST.get('contact')
        personal_profile = data.personal_profile if not request.POST.get('personal_profile') else request.POST.get(
            'personal_profile')
        ResumeData.objects.filter(username=current_user).update(job_title=job_title, email=email, contact=contact,
                                                                personal_profile=personal_profile)
        return redirect('resumes:edit')
    form = BasicForm()
    exp_form = ExperienceForm()
    edu_form = EducationForm()
    try:
        data = ResumeData.objects.get(username=current_user)
        print(data)
    except Exception:
        return redirect('login')
    user_data = cleandata(data)
    user_data.update({'form': form, 'exp_form': exp_form, 'edu_form': edu_form})
    return render(request, 'resume_form.html', context=user_data)


@login_required(login_url='login')
def workexperience(request):
    current_user = request.user
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        company_name = request.POST.get('company_name')
        start = request.POST.get('start')
        end = request.POST.get('end')
        responsibility = request.POST.get('responsibility', '')
        responsibility = responsibility.strip(' ').split('.')
        previous_data = ResumeData.objects.get(username=current_user)
        print(previous_data.work_experience)
        previous_data.work_experience = json.loads(previous_data.work_experience)
        if not previous_data.work_experience:
            previous_data.work_experience = []
        previous_data.work_experience.append({'company_name': company_name, 'start': start, 'end': end,
                                              'responsibility': responsibility})
        if form.is_valid():
            try:
                ResumeData.objects.filter(username=current_user).update(
                    work_experience=json.dumps(previous_data.work_experience))
                return redirect('resumes:edit')
            except:
                return render(request, 'error.html', {})


@login_required(login_url='login')
def education(request):
    current_user = request.user
    if request.method == 'POST':
        form = EducationForm(request.POST)
        college_name = request.POST.get('college_name')
        start = request.POST.get('start')
        end = request.POST.get('end')
        university = request.POST.get('university')
        qualification = request.POST.get('qualification')
        percentage = request.POST.get('percentage')
        previous_data = ResumeData.objects.get(username=current_user)
        previous_data.education = json.loads(previous_data.education)
        if not previous_data.education:
            previous_data.education = []
        previous_data.education.append({'college_name': college_name, 'start': start, 'end': end,
                                        'university': university, 'qualification': qualification,
                                        'percentage': percentage})

        if form.is_valid():
            try:
                ResumeData.objects.filter(username=current_user).update(education=json.dumps(previous_data.education))
                return redirect('resumes:edit')
            except:
                return render(request, 'error.html', {})


@login_required(login_url='login')
def skills(request):
    current_user = request.user

    if request.method == 'POST':
        skills = request.POST.get('key_skill', '')
        if skills.strip() is not '':
            skills = skills.strip().split(',')
        else:
            return redirect('resumes:edit')
        previous_data = ResumeData.objects.get(username=current_user)
        previous_data.key_skills = json.loads(previous_data.key_skills)
        if not previous_data.key_skills: previous_data.key_skills = []
        previous_data.key_skills.extend(skills)
        try:
            ResumeData.objects.filter(username=current_user).update(key_skills=json.dumps(previous_data.key_skills))
            return redirect('resumes:edit')
        except:
            return render(request, 'error.html', {})


@login_required(login_url='login')
def posts(request):
    current_user = request.user
    if request.method == 'POST':

        post_id = request.POST.get('post_id')
        post = request.POST.get('post')
        print(post, post_id)
        previous_data = ResumeData.objects.get(username=current_user)
        previous_data.post_qs = json.loads(previous_data.post_qs)
        previous_data.post_as = json.loads(previous_data.post_as)
        print(previous_data.post_as)
        if len(post) > 0 and len(previous_data.post_as) >= int(post_id) >= 0:
            previous_data.post_as[int(post_id)] = post
            try:
                ResumeData.objects.filter(username=current_user).update(post_as=json.dumps(previous_data.post_as))
                return redirect('resumes:edit')
            except Exception as e:
                print(e)
                return render(request, 'error.html', {})
        else:
            return redirect('resumes:edit')


class UserFormView(View):
    form_class = UserForm
    template_name = 'register.html'

    # dispalcy form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # cleaned data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            name = form.cleaned_data['first_name']
            contact = form.cleaned_data['contact']
            user.set_password(password)
            resume_data = ResumeData(username=username,
                                     name=name,
                                     email=email,
                                     contact=contact,
                                     job_title='',
                                     personal_profile='',
                                     work_experience='[]',
                                     key_skills='[]',
                                     education='[]')
            resume_data.save()
            user.save()
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('resumes:edit')
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    template_name = 'login.html'
    form_class = UserLogin

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('resumes:resume', username)
        return render(request, self.template_name, {'form': form, 'invalid': True})


def url_redirect(request):
    current_user = request.user
    print(current_user)
    if current_user.is_active:
        return redirect('resumes:resume', username=current_user.username)
    else:
        return redirect('login')
