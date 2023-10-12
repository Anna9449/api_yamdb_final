from django.core.mail import send_mail
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import MyUser
from users.serializers import TokenSerializer, SignUpSerializer


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer

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
    serializer_class = TokenSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        try:
            user = MyUser.objects.get(username=username)
        except MyUser.DoesNotExist:
            return Response(
                {'username': 'Not Found'},
                status=status.HTTP_404_NOT_FOUND
            )
        if confirmation_code == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)})
