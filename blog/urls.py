from django.urls import path
from . import views
from .views import CustomLoginView
from .views import signup_view


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path("signup/", signup_view, name="signup"),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path("reset/<uidb64>/<token>/", views.password_reset_confirm, name="password_reset_confirm"),
    path("register/", views.register, name='register'),
]
