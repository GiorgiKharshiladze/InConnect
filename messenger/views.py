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

def getData(request, typeOf):
	url 		= "http://" + request.get_host() + "/api/" + typeOf +"/?format=json"
	jsonurl 	= urlopen(url)
	data		= json.loads(jsonurl.read())
	return data

def response(request, sender_id, sender_response):
	isIn = False
	for user in getData(request, "users"):
		if user['sender_id'] == sender_id:
			isIn = True

	if not isIn:
		new_user = User(sender_id=sender_id, topic=sender_response)
		new_user.save()





VERIFY_TOKEN = '12345678'
PAGE_ACCESS_TOKEN = "EAAK5tc826v8BACZAudQd8vZByLNgod6W7f99ZCpZCGXAEXZAvIjvWBhAciO7eaxmTBwtpxKQJuqkU5b8ovlfSeyOGDkBDz8dGfQIhtCF15gytQ11wfZCUhuds2x4ceSFKYBeGyZCVPhTBnmwCWXIL3Br2c8zTzpcxgv1JGQ54x6Fofwx3C5wBMa"
DEFAULT_RESPONSE = "Please wait"

jokes = { 'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
					"""Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""], 
		'fat':		["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
				""" Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
		'dumb': ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
			"""Yo' Mama is so dumb, she locked her keys inside her motorcycle."""]}
# yomamabot/fb_yomamabot/views.py
# This function should be outside the BotsView class
def post_facebook_message(fbid, recevied_message):
	# Remove all punctuations, lower case the text and split it based on space
	# tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
	# joke_text = ''
	# for token in tokens:
	# 	if token in jokes:
	# 		joke_text = random.choice(jokes[token])
	# 		break
	# if not joke_text:
	# 	joke_text = "I didn't understand! Send 'stupid', 'fat', 'dumb' for a Yo Mama joke!"
	
	user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
	user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
	user_details = requests.get(user_details_url, user_details_params).json()
	# joke_text = 'Yo '+user_details['first_name']+'..! ' + joke_text
	joke_text = recevied_message

	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	# pprint(status.json())
def generate_message(request, message):
	another_user_id = getConnection(message['sender']['id'])
	if another_user_id == None:
		post_facebook_message(message['sender']['id'], DEFAULT_RESPONSE)
	else:
		post_facebook_message(another_user_id, message['message']['text'])

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

class MessageList(APIView):
	"""
	List all the messages as a RESTapi
	"""
	def get(self, request):
		messages = MessageModel.objects.all() # CourseModel located in serializers
		serializer = MessageSerializer(messages, many = True)

		return Response(serializer.data)