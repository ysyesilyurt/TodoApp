from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    re_path(r"^todolist/(?P<listID>[0-9]+)$", views.todos, name='todos'),
    re_path(r'^signup/$', views.signup, name='signup'),
]