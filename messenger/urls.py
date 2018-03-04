from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from messenger import views

urlpatterns = [
	url(r'^result/$', views.api, name='result'),
	url(r'^suggestions/$', views.SuggestionList.as_view(), name="suggestions"),
	url(r'^users/$', views.UserList.as_view(), name="users"),
	url(r'^chats/$', views.ChatList.as_view(), name="messages"),
	url(r'^chat/?$', views.InConnectBotView.as_view(), name="chat")
]

urlpatterns = format_suffix_patterns(urlpatterns)

