from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authorities', views.authorities, name='authorities'),
    path('authorities/create', views.create_authority, name='create_authority'),
    path('authorities/<int:authority_id>', views.show_authority, name='show_authority'),
    path('authorities/<int:authority_id>/edit', views.edit_authority, name='edit_authority'),
    path('authorities/delete', views.delete_authority, name='delete_authority'),
    path('authorities/<int:authority_id>/ca-certs/create', views.create_authority_ca_cert, name='create_authority_ca_cert'),
    path('authorities/<int:authority_id>/ca-certs/<int:certificate_id>', views.show_authority_ca_cert, name='show_authority_ca_cert'),
    path('authorities/<int:authority_id>/ca-certs/<int:certificate_id>/edit', views.edit_authority_ca_cert, name='edit_authority_ca_cert'),
    path('authorities/<int:authority_id>/ca-certs/delete', views.delete_authority_ca_cert, name='delete_authority_ca_cert'),
]