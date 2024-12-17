from django import forms
from .models import *

class TrackerForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=Profile.objects.all(), required=True, label="Users")
    class Meta:
        model = Trackers
        fields = ['tracker_name', 'url', 'user']  # Include the 'user' field



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'phonenumber', 'created_by','status']

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriptions
        fields = ['plan_name', 'start_date', 'end_date', 'trigger_limit']
