from django.contrib import admin
from django.urls import path,include
from home.views import *
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'people',Peopleview,basename="people")
urlpatterns=router.urls

urlpatterns = [
    path('',include(router.urls)),
    path('index/',index),
    path('person/',person),
    path('login/',login),
    path('register/',RegisterAPI.as_view()),
    path('personAPI/',PersonAPI.as_view()),
    path('Login/',LoginAPI.as_view())
    
]
