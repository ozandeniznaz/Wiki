from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="index"),
    path("wiki/entry/<str:title>/", views.entry, name="entry"),
    path("wiki/search/", views.search, name="q"),
    path("wiki/search/<str:title>/", views.entry, name="entry"),
    path("wiki/new-entry/", views.new_entry, name="new-entry"),
    path("wiki/entry/<str:title>/edit/", views.edit, name="edit"),
    path("wiki/random", views.random_entry, name="random"),
    ]