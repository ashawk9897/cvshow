from django.urls import path
from . import views
from django.views.generic import RedirectView

app_name = 'resumes'
urlpatterns = [
    path('', views.url_redirect, name='null'),
    path('resume/<str:username>', views.home, name='resume'),
    path('edit', views.editmode, name='edit'),
    path('edit/work', views.workexperience, name='work'),
    path('edit/edu', views.education, name='edu'),
    path('edit/skills', views.skills, name='skills'),
    path('edit/posts', views.posts, name='posts')
]
