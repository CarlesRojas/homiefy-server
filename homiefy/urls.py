"""homiefy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from userData import views



urlpatterns = []

urlpatterns.extend([
    #url(r'^admin/', admin.site.urls),
    url(r'^', include('userData.urls')),
    url(r'^', include('fileManager.urls')),
    #url(r'^login/emailCheck/$', views.TestAPI.as_view()),
])


urlpatterns.extend([
    url(r'^docs/', include('rest_framework_swagger.urls')),
])
