from django.db import models

class Suggestion(models.Model):

	id 				= models.AutoField(max_length = 5, primary_key = True)
	text 			= models.CharField(max_length = 255)
	type			= models.IntegerField(default=1)
	created_at 		= models.DateTimeField(auto_now_add=True, null=True)
	updated_at 		= models.DateTimeField(auto_now=True, null=True)


	def __str__(self): # Value that we see in DJANGO ADMIN
		return self.text

	class Meta:
		db_table = "suggestions" # Table name in DB
