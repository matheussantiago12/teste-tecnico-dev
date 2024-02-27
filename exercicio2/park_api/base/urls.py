from django.urls import path

from . import views

urlpatterns = [
    path('customers/', views.ListCustomers.as_view(), name="list_customers"),
    path('customers/', views.CreateCustomers.as_view(), name="create_customers"),
]