import json, requests, random, re
from pprint import pprint

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.views import generic
# import rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from messenger.serializers import *

VERIFY_TOKEN = '12345678'
class InConnectBotView(generic.View):

	def get(self, request, *args, **kwargs):
		if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Error, invalid token')

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