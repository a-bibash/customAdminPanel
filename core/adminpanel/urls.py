
from django.urls import path
from .views import *


urlpatterns = [
    path('',ad_dashboard, name ='ad_dashboard'),
    path('ad-user-list/',ad_user_list, name ='ad_user_list'),
    path('ad-tracker-list/',ad_tracker_list, name ='ad_tracker_list'),

    path('ad-tracker-list/edit_tracker/<int:tracker_id>/', edit_tracker, name='edit_tracker'),
    path('ad-user-list/edit_user/<int:user_id>/', edit_user, name='edit_user'),

    path('ad-tracker-list/delete_tracker/<int:tracker_id>/', tracker_delete, name='tracker_delete'),
    path('ad-user-list/delete_user/<int:user_id>/', user_delete, name='user_delete'),
    
    path('ad-tracker-list/add_tracker/', add_tracker, name='add_tracker'),

    path('ad-user-list/user_tracker_details/<int:user_id>/', user_tracker_details, name='user_tracker_details'),
]





# from django.urls import path
# from . import views

# urlpatterns = [
#     # Existing URLs
#     path('trackers/', views.tracker_list, name='tracker_list'),
#     path('trackers/<int:id>/detail/', views.tracker_detail, name='tracker_detail'),
#     path('trackers/<int:id>/edit/', views.tracker_edit, name='tracker_edit'),
#     path('trackers/<int:id>/delete/', views.tracker_delete, name='tracker_delete'),
#     path('trackers/<int:id>/configure/', views.tracker_configure, name='tracker_configure'),
# ]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('users/', views.UserListView.as_view(), name='user_list'),
#     path('user/edit/<int:id>/', views.UserEditView.as_view(), name='user_edit'),
#     path('user/delete/<int:id>/', views.UserDeleteView.as_view(), name='user_delete'),
# ]
