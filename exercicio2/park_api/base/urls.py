from django.urls import path

from . import views

urlpatterns = [
    path('customer/', views.CustomersView.as_view()),
    path('customer/<int:pk>/', views.CustomersDetailView.as_view()),
    path('vehicle/', views.VehiclesView.as_view()),
    path('vehicle/<int:pk>/', views.VehiclesDetailView.as_view()),
    path('plan/', views.PlansView.as_view()),
    path('plan/<int:pk>/', views.PlansDetailView.as_view()),
    path('contract/', views.ContractView.as_view()),
    path('parkmovement/', views.ParkMovementView.as_view()),
    path('parkmovement/<int:pk>/', views.ParkMovementDetailView.as_view()),
]