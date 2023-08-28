from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home_page'),
    path('groups/', views.Group_List.as_view(), name='group_list'),
    path('groups/<slug:slug>', views.Group_Detail.as_view(), name='group_detail'),
    path('create_group/', views.CreateGroupView.as_view(), name='group_create'),
    path('user_profile/<str:username>', views.UserProfileView.as_view(), name='user_profile'),
    path('join_group/<slug:slug>/', views.join_group, name='join_group'),
    path('leave_group/<slug:slug>/', views.leave_group, name='leave_group'),
    path('<slug:slug>/delete/', views.delete_group, name='delete_group'),
    path('delete/<int:pk>', views.post_delete, name='post_delete'),
]