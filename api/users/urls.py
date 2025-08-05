from django.urls import path
from api.users.views import RegisterView, LoginView, UserDetailView, RefreshTokenView
from rest_framework_simplejwt.views import TokenBlacklistView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('refresh/', RefreshTokenView.as_view(), name='token-refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='token-blacklist'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
]
