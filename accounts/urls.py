from django.urls import path
from django.contrib.auth.views import (LoginView, LogoutView, LogoutView)

from .views import AccountCreation, Payment, login,UpdateProfile

app_name = 'accounts'

urlpatterns = [
    path('signup/', AccountCreation.as_view(), name='signup'),
    path('payment/', Payment.as_view(), name='payment'),
    # path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('login/', login, name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/login.html'), name='logout'),
    # path('change_password/', change_password, name='change_password'),
    path('update/<pk>',UpdateProfile.as_view(),name='update-profile'),
]
