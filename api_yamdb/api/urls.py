from django.urls import include, path
from rest_framework import routers

from api.views import (
    CategoryViewSet, CommentViewSet, GenreViewSet,
    ReviewViewSet, TitleViewSet,
)

app_name = "api"

v1_router = routers.DefaultRouter()
v1_router.register("titles", TitleViewSet, basename="title")
v1_router.register("genres", GenreViewSet, basename="genre")
v1_router.register("categories", CategoryViewSet, basename="category")
v1_router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
v1_router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

v1_urls = [
    path("", include(v1_router.urls)),
]

urlpatterns = [
    path("v1/", include(v1_urls)),

]
