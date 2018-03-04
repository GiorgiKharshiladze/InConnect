from django.db import models

class Suggestion(models.Model):

	id 				= models.AutoField(max_length = 5, primary_key = True)
	text 			= models.CharField(max_length = 255)
	type			= models.IntegerField(default=1)
	created_at 		= models.DateTimeField(auto_now_add=True, null=True)
	updated_at 		= models.DateTimeField(auto_now=True, null=True)


	def __str__(self): # Value that we see in DJANGO ADMIN
		return str(self.id) + ": " +self.text

	class Meta:
		db_table = "suggestions" # Table name in DB

class User(models.Model):

	id 				= models.AutoField(max_length = 5, primary_key = True)
	sender_id 		= models.CharField(max_length = 255)
	topic			= models.CharField(max_length = 255)
	created_at 		= models.DateTimeField(auto_now_add=True, null=True)
	updated_at 		= models.DateTimeField(auto_now=True, null=True)

	def __str__(self): # Value that we see in DJANGO ADMIN
		return str(self.id) + ": " +self.sender_id + " (" + self.topic + ")"

	class Meta:
		db_table = "users" # Table name in DB

class Chat(models.Model):
	
	id 				= models.AutoField(max_length = 30, primary_key = True)
	sender_one 		= models.CharField(max_length = 255)
	sender_two 		= models.CharField(max_length = 255)
	topic 			= models.CharField(max_length = 255, null=True)
	status			= models.BooleanField(default=False)
	created_at 		= models.DateTimeField(auto_now_add=True, null=True)
	updated_at 		= models.DateTimeField(auto_now=True, null=True)

	def __str__(self): # Value that we see in DJANGO ADMIN
		return "Chat_Id: " + str(self.id) + " - " + self.sender_one + " and " + self.sender_two

	class Meta:
		db_table = "chats" # Table name in DB

# class Message(models.Model):

# 	id 				= models.AutoField(max_length = 30, primary_key = True)
# 	chat_id			= models.IntegerField(unique = True)
# 	sender_one 		= models.CharField(max_length = 255)
# 	sender_two 		= models.CharField(max_length = 255)
# 	message 		= models.TextField(null=True)
# 	created_at 		= models.DateTimeField(auto_now_add=True, null=True)
# 	updated_at 		= models.DateTimeField(auto_now=True, null=True)

	# def __str__(self): # Value that we see in DJANGO ADMIN
	# 	return "Chat_Id: " + str(self.chat_id) + " Message: " + message

	# class Meta:
	# 	db_table = "messages" # Table name in DB