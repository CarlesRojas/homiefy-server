from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from userData import views


urlpatterns = [
   url(r'^utilities/$', views.utilities.as_view()),
   url(r'^balance/add/$', views.AddBalance.as_view()),
   url(r'^balance/$', views.Balance.as_view()),
   url(r'^postits/$', views.Postit.as_view()),
   url(r'^list/$', views.List.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)