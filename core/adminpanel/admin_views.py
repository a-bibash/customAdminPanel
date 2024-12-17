# adminpanel/admin_views.py
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin
from django.http import HttpResponse

from .models import Profile  # Your model

@staff_member_required
def custom_admin_view(request):
    profiles = Profile.objects.all()  # Fetch profiles from the database
    context = {
        'profiles': profiles,
    }
    return render(request, 'adminpanel/admin.html', context)
