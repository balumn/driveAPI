# pages/urls.py
# from django.urls import path
from django.conf.urls import url,include


from . import views

urlpatterns = [
    url(r'^about/', views.about, name='pages'),
    url('', views.homme, name='home'),

]