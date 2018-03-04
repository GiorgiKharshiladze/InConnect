import json, requests, random, re
from urllib.request import urlopen
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
from .models import User
from .messenger import Messenger


VERIFY_TOKEN = '12345678'
PAGE_ACCESS_TOKEN = "EAAK5tc826v8BACZAudQd8vZByLNgod6W7f99ZCpZCGXAEXZAvIjvWBhAciO7eaxmTBwtpxKQJuqkU5b8ovlfSeyOGDkBDz8dGfQIhtCF15gytQ11wfZCUhuds2x4ceSFKYBeGyZCVPhTBnmwCWXIL3Br2c8zTzpcxgv1JGQ54x6Fofwx3C5wBMa"
DEFAULT_RESPONSE_FOR_WAIT = "Please wait"
DEFAULT_RESPONSE_FOR_START = 

class InConnectBotView(generic.View):

	def get(self, request, *args, **kwargs):
		if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Error, invalid token')

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		# Converts the text payload into a python dictionary
		incoming_message = json.loads(self.request.body.decode('utf-8'))
		# Facebook recommends going through every entry since they might send
		# multiple messages in a single call during high load
		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				# Check to make sure the received call is a message call
				# This might be delivery, optin, postback for other events 
				if 'message' in message:
					# Print the message to the terminal
					pprint(message)
					# Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
					# are sent as attachments and must be handled accordingly. 
					# post_facebook_message(message['sender']['id'], message['message']['text'])
					addUser(request, message['sender']['id'], message['message']['text'])
					# addUserChat(request, message)
					generate_message(request, message)
					# post_facebook_message(message['sender']['id'], response(request, message['sender']['id'], message['message']['text']))

		return HttpResponse()

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

	def post(self, request, format=None):
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatList(APIView):
	"""
	List all the chats as a RESTapi
	"""
	def get(self, request):
		chats = ChatModel.objects.all() # CourseModel located in serializers
		serializer = ChatSerializer(chats, many = True)

		return Response(serializer.data)