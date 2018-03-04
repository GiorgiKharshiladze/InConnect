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
from .models import User, Chat

VERIFY_TOKEN = '12345678'
PAGE_ACCESS_TOKEN = "EAAK5tc826v8BACZAudQd8vZByLNgod6W7f99ZCpZCGXAEXZAvIjvWBhAciO7eaxmTBwtpxKQJuqkU5b8ovlfSeyOGDkBDz8dGfQIhtCF15gytQ11wfZCUhuds2x4ceSFKYBeGyZCVPhTBnmwCWXIL3Br2c8zTzpcxgv1JGQ54x6Fofwx3C5wBMa"
DEFAULT_RESPONSE_FOR_WAIT = "Please wait"
DEFAULT_RESPONSE_FOR_START = "You can start your conversation"

def getData(request, type_of):
	url 		= "http://" + request.get_host() + "/api/" + type_of +"/?format=json"
	jsonurl 	= urlopen(url)
	data		= json.loads(jsonurl.read())
	return data

def getTopic(sender_id):	
	my_user = User.object.get(sender_id = sender_id)
	return my_user['topic']

def setChatUser(chat_id, sender_two_id):
	my_chat = Chat.object.get(id=chat_id)
	my_chat['sender_two'] = sender_two_id
	my_chat.save()

def createChat(sender_one_id):
	topic = getTopic(sender_one_id)
	new_chat = Chat(sender_one=sender_one_id, topic=topic)
	new_chat.save()

def addUser(request, sender_id, sender_response):
	isIn = False
	for user in getData(request, "users"):
		if user['sender_id'] == sender_id:
			isIn = True

	if not isIn:
		new_user = User(sender_id=sender_id, topic=sender_response)
		new_user.save()

def addUserChat(request, message):

	sender_id = message['sender']['id']

	for chat in getData(request, "chats"):
		if chat['status'] == False and getTopic(sender_id) == chat['topic']:
			setChatUser(chat['id'], sender_id)
			break

	createChat(sender_id)

def generateMessage(request, message):
	another_user_id = getConnection(request, message['sender']['id'])
	if another_user_id == None:
		sendMessage(message['sender']['id'], DEFAULT_RESPONSE_FOR_WAIT)
	else:
		sendMessage(another_user_id, message['message']['text'])

def getConnection(request, sender_id):

	for chat in getData(request, "chats"):
		if chat['sender_one'] == sender_id:
			return chat['sender_two']
		elif chat['sender_two'] == sender_id:
			return chat['sender_one']

	return None

# # This function should be outside the BotsView class
def sendMessage(fbid, recieved_message):
	# Remove all punctuations, lower case the text and split it based on space
	tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recieved_message).lower().split()
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

	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recieved_message}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	# pprint(status.json())
