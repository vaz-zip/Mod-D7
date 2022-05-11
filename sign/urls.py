from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import Update_profile, BaseRegisterView, Account, add_authors

urlpatterns = [
    path('account/', Account.as_view()),
    path('add_authors/', add_authors, name = 'upgrade'),
    path('login/', LoginView.as_view(template_name = 'sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name = 'sign/logout.html'), name='logout'),
    path('edit/', Update_profile.as_view(template_name = 'sign/update_profile.html'), name='user_update'),
    path('signup/', BaseRegisterView.as_view(template_name = 'sign/signup.html'), name='signup'),
]