from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name="about"),
    path('contact/', views.ContactView.as_view(), name="contact"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('update/<int:pk>/', views.UpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.DeleteView.as_view(), name='delete'),
    path('confirm/', views.ConfirmView.as_view(), name='confirm'),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('donor-profile/<int:pk>/', views.DonorView.as_view(), name='donor-profile'),
    path('donorlist/', views.DonorListView.as_view(), name="donorlist"),
    path('healthtips/', views.HealthTipsView.as_view(), name="healthtips"),
]
