from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.db.models import Sum, Count
from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


# @login_required
def ad_dashboard(request):
    users_with_tracker_and_trigger = Profile.objects.annotate(
        total_triggers=Sum('subscriptions__trigger_limit',
                           distinct=True),  # Sum distinct trigger limits
        total_trackers=Count('trackers')
    )[:10]
    trackers = Trackers.objects.all()[:10]
    return render(request, 'adminpanel/dashboard.html', {
        'users': users_with_tracker_and_trigger,
        'trackers': trackers
    })

# @login_required


def ad_user_list(request):
    query = request.GET.get('q', '')  # Get the search query
    users_with_tracker_and_trigger = Profile.objects.annotate(
        total_triggers=Sum('subscriptions__trigger_limit', distinct=True),
        total_trackers=Count('trackers')
    )
    # Filter users based on the search query
    if query:
        users_with_tracker_and_trigger = users_with_tracker_and_trigger.filter(
            user__username__icontains=query)

    return render(request, "adminpanel/ad-profile.html", {
        'users': users_with_tracker_and_trigger,
        'search_query': query
    })



# @login_required
def ad_tracker_list(request):
    search_query = request.GET.get('q', '')  # Retrieve search query, default to empty string
    trackers = Trackers.objects.all()

    # Filter trackers based on search query: tracker_name, tracker_id, or user.username
    if search_query:
        trackers = trackers.filter(
            Q(tracker_id__icontains=search_query) | 
            Q(tracker_name__icontains=search_query) | 
            Q(user__user__username__icontains=search_query)  # Search on related user's username
        )

    return render(request, "adminpanel/ad-tracker.html", {
        'trackers': trackers,
        'search_query': search_query,  # Pass search_query back to the template
    })


# @login_required
def edit_user(request, user_id):
    profile = get_object_or_404(Profile, id=user_id)

    # Get the associated subscription
    subscription = Subscriptions.objects.filter(profile=profile).first()

    if request.method == 'POST':
        # Create forms with the POST data
        profile_form = ProfileForm(request.POST, instance=profile)
        subscription_form = SubscriptionForm(
            request.POST, instance=subscription)

        if profile_form.is_valid() and subscription_form.is_valid():
            # Save both forms
            profile_form.save()
            subscription_form.save()
            # Redirect to a profile detail page or dashboard
            return redirect('ad_user_list')

    else:
        # Pre-fill the form with current data
        profile_form = ProfileForm(instance=profile)
        subscription_form = SubscriptionForm(instance=subscription)

    return render(request, 'adminpanel/edit_user.html', {
        'profile_form': profile_form,
        'subscription_form': subscription_form,
        'profile': profile
    })


# @login_required
def edit_tracker(request, tracker_id):
    tracker = get_object_or_404(Trackers, tracker_id=tracker_id)

    if request.method == 'POST':
        form = TrackerForm(request.POST, instance=tracker)
        if form.is_valid():
            tracker = form.save(commit=False)

            # Assign user from the form
            tracker.user = form.cleaned_data['user']
            tracker.save()
            return redirect('ad_tracker_list')
        else:
            print("Form Errors: ", form.errors)  # Debugging errors
    else:
        form = TrackerForm(instance=tracker)

    return render(request, 'adminpanel/edit_tracker.html', {'form': form, 'tracker': tracker})


# @login_required
def tracker_delete(request, tracker_id):
    # Fetch the tracker using tracker_id
    tracker = get_object_or_404(Trackers, tracker_id=tracker_id)
    tracker.delete()

    return redirect('ad_tracker_list')  # Redirect to the list view


# @login_required
def user_delete(request, user_id):

    user = get_object_or_404(Profile, id=user_id)

    # if not request.user.is_staff and request.user != user:
    #     return redirect('permission_denied')
    user.delete()
    return redirect('ad_user_list')


# @login_required
def add_tracker(request):
    if request.method == 'POST':
        form = TrackerForm(request.POST)
        if form.is_valid():
            tracker = form.save(commit=False)
            # Assign user from the form
            tracker.user = form.cleaned_data['user']
            tracker.save()
            return redirect('ad_tracker_list')
    else:
        form = TrackerForm()

    return render(request, 'adminpanel/add_tracker.html', {'form': form})


def user_tracker_details(request, user_id):
    # Fetch the user's profile and related trackers
    user_profile = get_object_or_404(Profile, id=user_id)
    trackers = Trackers.objects.filter(
        user=user_profile)  # Fetch trackers for this user

    return render(request, 'adminpanel/user_tracker_details.html', {
        'user_profile': user_profile,
        'trackers': trackers
    })
