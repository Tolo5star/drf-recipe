from django.urls import path
from .views import CreateUserView, CreateTokenView, UserProfileView


app_name = 'user'
urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
