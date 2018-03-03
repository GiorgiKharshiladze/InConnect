from rest_framework import serializers
from .models import Suggestion as SuggestionModel, User as UserModel, Message as MessageModel

class SuggestionSerializer(serializers.ModelSerializer):

	class Meta:
		model = SuggestionModel
		fields = "__all__"

class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = UserModel
		fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):

	class Meta:
		model = MessageModel
		fields = "__all__"