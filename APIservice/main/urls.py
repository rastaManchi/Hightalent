from django.urls import path
from . import views

urlpatterns = [
    path('questions/', views.question_list),
    path('questions/<int:id>/', views.question_detail),
    path('questions/<int:id>/answers/', views.answer_list),
    path('answers/<int:id>/', views.answer_detail),
]
