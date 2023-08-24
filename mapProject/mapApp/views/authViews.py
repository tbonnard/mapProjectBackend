from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.http import Http404
from rest_framework import status
from django.contrib.auth import authenticate, login
import os
from django.http import JsonResponse

import jwt, datetime
from django.middleware import csrf

from ..serializers import UsersSerializer, UserDetailsSerializer
from ..models import User
from ..utils.validateUserPerm import validate_if_authenticated, validate_superuser


class RegisterView(APIView):
    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        # To validate and if not, raises an exception
        serializer.is_valid(raise_exception=True)
        serializer.save()
        userLoggedIn = LoginView.post(self, request)
        return userLoggedIn


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('user not found')

        if not user.check_password(password):
            raise AuthenticationFailed('incorrect password')

        user = authenticate(email=email, password=password)
        if user is not None and user.is_active:
            request.user = user
        else:
            raise AuthenticationFailed('user not authenticated')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        SECRET_KEY_AUTH_APP= os.environ.get("SECRET_KEY_AUTH_APP")
        token = jwt.encode(payload, SECRET_KEY_AUTH_APP, algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwtTk', value=token, httponly=True, samesite='Lax', path="/", domain='localhost:3000', expires=datetime.datetime.utcnow() + datetime.timedelta(days=1))

        csrf_token = csrf.get_token(request)
        response.set_cookie(key='csrftoken', value=csrf_token, path="/")

        serializer = UserDetailsSerializer(user)

        response.data = {
            'jwt': token,
            # 'csrftoken': csrf_token,
            'user':serializer.data
        }
        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwtTk')
        response.data = {
            'message':'Success'
        }
        return response


class UserAuthView(APIView):
    """
    Retrieve, update or delete the authenticated instance.
    """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        user = request.user
        #data_authenticated_user = validate_if_authenticated(request)
        #if data_authenticated_user['authenticated']:
        instance = self.get_object(user.id)
        serializer = UserDetailsSerializer(instance)
        return Response(serializer.data)
        #raise AuthenticationFailed('Unauthenticated')

    def put(self, request, format=None):
        data_authenticated_user = validate_if_authenticated(request)
        if data_authenticated_user['authenticated']:
            instance = self.get_object(data_authenticated_user['user'].id)
            serializer = UserDetailsSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise AuthenticationFailed('Unauthenticated')

    def delete(self, request, format=None):
        data_authenticated_user = validate_if_authenticated(request)
        if data_authenticated_user['authenticated']:
            instance = self.get_object(data_authenticated_user['user'].id)
            instance.delete()
            return Response('Data erased', status=status.HTTP_204_NO_CONTENT)
        raise AuthenticationFailed('Unauthenticated')



class UsersAPIView(APIView):
    """
    Retrieve all instances.
    For superuser only
    """
    def get(self, request, *args, **kwargs):
        data_authenticated_user = validate_if_authenticated(request)
        if data_authenticated_user['authenticated']:
            if validate_superuser(data_authenticated_user['user']):
                users = User.objects.all()
                serializer = UsersSerializer(users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)
        raise AuthenticationFailed('Incorrect rights')


class UserView(APIView):
    """
    Retrieve, update or delete an instance.
    For superuser only
    """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data_authenticated_user = validate_if_authenticated(request)
        if data_authenticated_user['authenticated']:
            if validate_superuser(data_authenticated_user['user']):
                instance = self.get_object(pk)
                serializer = UserDetailsSerializer(instance)
                return Response(serializer.data)
            return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)
        raise AuthenticationFailed('Unauthenticated')

    def put(self, request, pk, format=None):
        data_authenticated_user = validate_if_authenticated(request)
        if data_authenticated_user['authenticated']:
            if data_authenticated_user['user'].is_superuser:
                instance = self.get_object(pk)
                serializer = UserDetailsSerializer(instance, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)
        raise AuthenticationFailed('Unauthenticated')

    def delete(self, request, pk, format=None):
        data_authenticated_user = validate_if_authenticated(request)
        if data_authenticated_user['authenticated']:
            if validate_superuser(data_authenticated_user['user']):
                instance = self.get_object(pk)
                instance.delete()
                return Response('No data', status=status.HTTP_204_NO_CONTENT)
            return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)
        raise AuthenticationFailed('Unauthenticated')