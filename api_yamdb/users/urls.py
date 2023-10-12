from django.urls import path

from users.views import SignUpView, TokenCreateView


urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', TokenCreateView.as_view(), name='token'),
]
