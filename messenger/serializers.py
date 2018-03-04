from rest_framework import serializers
from .models import Suggestion as SuggestionModel, User as UserModel, Chat as ChatModel

class SuggestionSerializer(serializers.ModelSerializer):

	class Meta:
		model = SuggestionModel
		fields = "__all__"

class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = UserModel
		fields = "__all__"

class ChatSerializer(serializers.ModelSerializer):

	class Meta:
		model = ChatModel
		fields = "__all__"