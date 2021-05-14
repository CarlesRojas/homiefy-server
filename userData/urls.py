from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from userData import views


urlpatterns = [
   url(r'^userData/debts/$', views.debts.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)