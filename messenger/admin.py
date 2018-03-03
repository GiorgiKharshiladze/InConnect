from django.contrib import admin
from .models import Suggestion

admin.register(Suggestion)(admin.ModelAdmin)