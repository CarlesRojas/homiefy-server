from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from fileManager import views


urlpatterns = [
   url(r'^fileManager/profilePic', views.profilePic.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)