from django.conf.urls import url
from adsgen import views

urlpatterns = [
    url('', views.home)
]
