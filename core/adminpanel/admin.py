# adminpanel/admin.py
from django.contrib import admin
from django.urls import path
from .models import *  # Replace with your actual model

# Register models
admin.site.register(Profile)  # Register your models
admin.site.register(Subscriptions)
admin.site.register(Trackers)
