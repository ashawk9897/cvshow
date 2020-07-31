"""iresume URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import logout #password_reset, password_reset_confirm, password_reset_done
from django.contrib.auth.views import PasswordResetView,LogoutView
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from resumes.views import UserLoginView,UserFormView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('resumes.urls')),
    url(r'^login/$', UserLoginView.as_view(), name='login'),
    url(r'^logout/$',LogoutView.as_view(),name='logout'),
    url(r'^register/$', UserFormView.as_view(), name='register'),
    url('^', include('django.contrib.auth.urls')),
    # url(r'^reset_password/$', password_reset, {'template_name': 'dashboard/reset_password.html'},
    #     name='password_reset'),
    # url(r'^reset_password/done/$', password_reset_done, {'template_name': 'dashboard/password_reset_done.html'},
    #     name='password_reset_done'),
    # url(r'^reset_password/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     password_reset_confirm, {'template_name': 'dashboard/password_reset_confirm.html'},
    #     name='password_reset_confirm'),
    # url(r'^reset_password/complete/$',RedirectView.as_view(url=reverse_lazy('login'), permanent=False), name='password_reset_complete'),

]
