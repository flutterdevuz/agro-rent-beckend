from users.views import (
    LoginView, RegisterView, ResetPasswordView,
    ProfileView, UpdateProfileView, UserOrdersView,
    UserListView, DashboardStatsView
)
from django.urls import path

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='profile-update'),
    path('orders/', UserOrdersView.as_view(), name='user-orders'),
    path('list/', UserListView.as_view(), name='user-list'),
    path('stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
]
