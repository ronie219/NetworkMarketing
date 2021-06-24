from django.urls import path

from .views import Profile,ListOfUser,ApproveList,DeleteUser,approveUser

app_name = 'management'

urlpatterns = [
    path('profile/', Profile.as_view(), name='profile'),
    path('user-list/', ListOfUser.as_view(), name='user-list'),
    path('approve/',ApproveList.as_view(),name='approve'),
    path('delete/<pk>',DeleteUser.as_view(),name='delete'),

    path('approve-user/<pk>',approveUser,name='approve-user')
]
