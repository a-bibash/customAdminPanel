from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Profile model - Extended user information


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phonenumber = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    ward_number = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[(
        'Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="profiles_created")
    status = models.CharField(max_length=20, choices=[(
        'active', 'Active'), ('inactive', 'Inactive')], default='active')

    def __str__(self):
        return f"{self.user}"

    class Meta:
        db_table = 'profile'


class Subscriptions(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True)  # Linking to Profile
    plan_name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=8, blank=True, null=True)
    trigger_limit = models.IntegerField(
        blank=True, null=True, default=10)  # Default trigger_limit is 10

    class Meta:
        db_table = 'subscriptions'  # Custom table name

    def __str__(self):
        return f"Subscription for {self.profile.user.username} - {self.plan_name}"


class Trackers(models.Model):
    tracker_id = models.AutoField(primary_key=True)
    tracker_name = models.CharField(max_length=255)
    url = models.CharField(max_length=2083)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'trackers'
        # Ensure the tracker_name + url combination is unique per user
        unique_together = ('tracker_name', 'url', 'user')

    def __str__(self):
        return f"Tracker Name: {self.tracker_name} - {self.user}"
