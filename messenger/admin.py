from django.contrib import admin
from .models import Suggestion, User, Chat

admin.register(Suggestion, User, Chat)(admin.ModelAdmin)