from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('name/<str:name>', views.name, name='name'),
    path('image', views.image, name='image')
]