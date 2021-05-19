from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from authentication.serializers import UserSerializer, LoginSerializer
from django.contrib.auth.models import User

from authentication.permissions import HasGroupPermission
# Create your views here.

from rest_framework.permissions import IsAuthenticated

# from rest_framework.authtoken.models import Token

from rest_framework.authtoken.models import Token


from rest_framework.authentication import TokenAuthentication


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user=serializer.validated_data.get('user')
        user = serializer.validated_data['user']
        # user=validatedData['user']
        token, _ = Token.objects.get_or_create(user=user)
        # token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class UserList(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [HasGroupPermission]
    required_groups = {
        'GET': ['USER'],
        # 'POST': ['moderators', 'someMadeUpGroup'],
        # 'PUT': ['__all__'],
    }
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser]


# class MyView(APIView):
#     permission_classes = [HasGroupPermission]
#     required_groups = {
#         'GET': ['moderators', 'members'],
#         'POST': ['moderators', 'someMadeUpGroup'],
#         'PUT': ['__all__'],
#     }

#     ...


class ApiRoot(APIView):

    def get(self, request, format=None):

        return Response({

            'register': reverse('register', request=request, format=format),
            # 'hello':reverse('hello',request=request),

            'list': reverse('list', request=request, format=format),
            'login': reverse('login', request=request, format=format),
            # 'list': reverse('list', request=request, format=format),
            # 'mynotes': reverse('mynotes', request=request, format=format),
            # 'profile': reverse('profile', request=request, format=format),

        })
