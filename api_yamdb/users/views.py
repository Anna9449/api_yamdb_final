from django.core.mail import send_mail
from rest_framework import status, generics, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import MyUser
from users.serializers import (TokenSerializer, SignUpSerializer,
                               UserSerializer, NotAdminSerializer)
from users.permissions import AdminStaffOnly


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
        elif request.method == 'PATCH':
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
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response({'confirmation_code': 'Invalid Code'},
                        status=status.HTTP_400_BAD_REQUEST)
