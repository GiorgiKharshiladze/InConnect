class Messenger():

def getData(request, typeOf):
	url 		= "http://" + request.get_host() + "/api/" + typeOf +"/?format=json"
	jsonurl 	= urlopen(url)
	data		= json.loads(jsonurl.read())
	return data

def addUser(request, sender_id, sender_response):
	isIn = False
	for user in getData(request, "users"):
		if user['sender_id'] == sender_id:
			isIn = True

	if not isIn:
		new_user = User(sender_id=sender_id, topic=sender_response)
		new_user.save()

def addUserChat(request, message):
	for chat in getData(request, "chats"):
		if chat['status'] == False:
			# ar dagaviwydes TOPIC
			chat['sender_two'] = message['sender']['id']#


# yomamabot/fb_yomamabot/views.py
# This function should be outside the BotsView class
def post_facebook_message(fbid, recieved_message):
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

def getConnection(request, sender_id):

	for chat in getData(request, "chats"):
		if chat['sender_one'] == sender_id:
			return chat['sender_two']
		elif chat['sender_two'] == sender_id:
			return chat['sender_one']

	return None


def generate_message(request, message):
	another_user_id = getConnection(request, message['sender']['id'])
	if another_user_id == None:
		post_facebook_message(message['sender']['id'], DEFAULT_RESPONSE)
	else:
		post_facebook_message(another_user_id, message['message']['text'])
