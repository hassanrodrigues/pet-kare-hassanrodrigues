from . import views
from django.urls import path

urlpatterns = [
    path("pets/", views.PetView.as_view()),
    path("pets/<pet_id>/", views.PetDetailView.as_view()),
]
