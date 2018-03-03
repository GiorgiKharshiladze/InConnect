from django.shortcuts import render
from django.http import Http404, HttpResponse

# import rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from messenger.serializers import *

# Create your views here.
def api(request):
	return render(request, "index.html")


class SuggestionList(APIView):
	"""
	List all the suggestions as a RESTapi
	"""
	def get(self, request):
		suggestions = SuggestionModel.objects.all() # CourseModel located in serializers
		serializer = SuggestionSerializer(suggestions, many = True)

		return Response(serializer.data)

class UserList(APIView):
	"""
	List all the users as a RESTapi
	"""
	def get(self, request):
		users = UserModel.objects.all() # CourseModel located in serializers
		serializer = UserSerializer(users, many = True)

		return Response(serializer.data)

class MessageList(APIView):
	"""
	List all the messages as a RESTapi
	"""
	def get(self, request):
		messages = MessageModel.objects.all() # CourseModel located in serializers
		serializer = MessageSerializer(messages, many = True)

		return Response(serializer.data)