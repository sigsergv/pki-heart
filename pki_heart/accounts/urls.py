from django.urls import path

from . import views

urlpatterns = [
    # current account profile page
    path('', views.index, name='index'),

    path('login/', views.login, name = 'login'),
    path('logout', views.logout, name = 'logout'),
]