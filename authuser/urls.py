from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('signup/', views.UserSignUpView.as_view(), name='signup'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name='activate'),
]
