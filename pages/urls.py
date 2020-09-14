from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'admin_app'
urlpatterns = [
    path('', views.homePageView, name='homePageView'),
    # path('adminIndex', views.adminIndex, name='adminIndex'),
    path('drive/', views.googleDrive, name='googleDrive'),
    path('dropbox/', views.dropBox, name='dropBox'),
    path('login/', LoginView.as_view(template_name='admin_app/login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name='admin_app/login.html'), name='logout'),

    ]
