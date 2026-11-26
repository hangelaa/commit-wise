from django.urls import path

from . import views

urlpatterns = [
    path("", views.overview, name="overview"),
    path("commits/", views.commit_list, name="commits"),
    path("commits/<str:commit_id>/", views.commit_detail, name="detail"),
]
