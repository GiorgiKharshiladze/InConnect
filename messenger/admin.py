from django.contrib import admin
from .models import Suggestion, User, Message

admin.register(Suggestion, User, Message)(admin.ModelAdmin)