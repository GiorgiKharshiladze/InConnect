from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from messenger import views

urlpatterns = [
	url(r'^result/$', views.api, name='result'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

