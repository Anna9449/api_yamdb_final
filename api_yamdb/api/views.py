from django.core.exceptions import BadRequest
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import shortuuid

from api.filters import TitleFilter
from api.permissions import (AdminStaffOnly, IsAdminOrReadOnly,
                             IsAuthorModeratorAdminOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, NotAdminSerializer,
                             ReviewSerializer, SignUpSerializer,
                             TitleCreateSerializer, TitleSerializer,
                             TokenSerializer, UserSerializer)
from reviews.models import Categories, Genres, Review, Title
from users.models import MyUser


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    create_serializer_class = TitleCreateSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return self.create_serializer_class
        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().update(request, *args, **kwargs)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        if request.method == 'PATCH':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().update(request, *args, **kwargs)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly)
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    ]

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def update_rating(self):
        rating = self.get_queryset().aggregate(Avg('score'))
        return (Title.objects.filter(pk=self.kwargs.get('title_id'))
                .update(rating=int(rating['score__avg'])))

    def perform_create(self, serializer):
        obj = self.get_queryset().filter(
            author=self.request.user, title=self.get_title()
        )
        if obj.exists():
            raise BadRequest(
                'Вы уже опубликовали отзыв на это произведение!'
            )
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )
        self.update_rating()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly)
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    ]

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, AdminStaffOnly,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        serializer = NotAdminSerializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def send_conformation_email(self, user):
        user.confirmation_code = shortuuid.uuid()[:6]
        user.save()
        send_mail(
            subject='Confirmation Code',
            message=f'Your confirmation code: {user.confirmation_code}',
            from_email='from@example.com',
            recipient_list=[user.email],
            fail_silently=False
        )

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        username = request.data.get('username')
        try:
            user = MyUser.objects.get(username=username, email=email)
        except MyUser.DoesNotExist:
            if MyUser.objects.filter(email=email).exists():
                return Response({'detail': 'Email is already registered.'},
                                status=status.HTTP_400_BAD_REQUEST)
            if MyUser.objects.filter(username=username).exists():
                return Response({'detail': 'Username is already taken.'},
                                status=status.HTTP_400_BAD_REQUEST)
            user = None
        if user:
            self.send_conformation_email(user)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            self.send_conformation_email(user)
        return Response(
            {
                'email': user.email,
                'username': user.username
            }, status=status.HTTP_200_OK
        )


class TokenCreateView(generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = MyUser.objects.get(username=request.data.get('username'))
        except MyUser.DoesNotExist:
            return Response(
                {'username': 'Not Found'},
                status=status.HTTP_404_NOT_FOUND
            )
        if request.data.get('confirmation_code') == user.confirmation_code:
            user.confirmation_code = ''
            user.save()
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response({'confirmation_code': 'Invalid Code'},
                        status=status.HTTP_400_BAD_REQUEST)
