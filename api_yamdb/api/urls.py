from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import ReviewViewSet, CommentViewSet, TitleViewSet

router_v1 = DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='reviews'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
