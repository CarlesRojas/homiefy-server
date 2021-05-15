from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from userData import views


urlpatterns = [
   url(r'^userData/utilities/$', views.utilities.as_view()),
   url(r'^userData/balance/$', views.balance.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)