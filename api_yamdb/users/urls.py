from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from users.views import SignUpView, TokenCreateView, UserViewSet

app_name = 'users'

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', TokenCreateView.as_view(), name='token'),
    path('v1/', include(router_v1.urls)),
]
