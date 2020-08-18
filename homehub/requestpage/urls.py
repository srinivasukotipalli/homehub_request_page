from django.urls import path, include
from . import views

from rest_framework import routers
from requestpage import views


urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('', views.loginPage, name="login"),
	path('logout/', views.logoutUser, name="logout"),
	path('request/', views.RequestpageList.as_view(),name="home"),
	path('newrequest/', views.Newrequestpage, name="newrequestpage"),
	path('request/<int:pk>/', views.RequestpageDetail.as_view()),
]
