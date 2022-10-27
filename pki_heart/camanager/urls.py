from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authorities', views.authorities, name='authorities'),
    path('authorities/create', views.create_authority),
    path('authorities/delete', views.delete_authority),
]