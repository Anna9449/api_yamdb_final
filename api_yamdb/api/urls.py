
from django.urls import include, path
from rest_framework import routers

from api.views import TitleViewSet, GenreViewSet, CategoryViewSet

app_name = "api"

v1_router = routers.DefaultRouter()
v1_router.register("titles", TitleViewSet, basename="title")
v1_router.register("genres", GenreViewSet, basename="genre")
v1_router.register("categories", CategoryViewSet, basename="category")

v1_urls = [
    path("", include(v1_router.urls)),
]

urlpatterns = [
    path("v1/", include(v1_urls)),

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
