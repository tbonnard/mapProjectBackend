import requests
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import json
from django.http import Http404

from ..serializers import VoteSerializer
from ..models import Vote, Project, Property, User, Follow


class VoteView(APIView):
    def get(self, request):
        queryset = Vote.objects.all()
        if queryset is not None:
            serializer = VoteSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response('No data', status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        voteAlreadyCreated = Vote.objects.filter(property=Property.objects.get(pk=request.data['property']),
                                                         voter=User.objects.get(pk=request.data['voter']),
                                                 value=request.data['value'],
                                                 project=Project.objects.get(pk=request.data['project'])).first()
        if voteAlreadyCreated:
            return Response('Already created', status=status.HTTP_204_NO_CONTENT)
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VotePropertyView(APIView):
    def get(self, request, propertyid):
        queryset = Vote.objects.filter(property=Property.objects.get(pk=propertyid))
        if queryset is not None:
            serializer = VoteSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response('No data', status=status.HTTP_204_NO_CONTENT)


class VoteProjectView(APIView):
    def get(self, request, projectid):
        queryset = Vote.objects.filter(project=Project.objects.get(pk=projectid))
        if queryset is not None:
            serializer = VoteSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response('No data', status=status.HTTP_204_NO_CONTENT)


class VotePropertyUserView(APIView):
    def post(self, request):
        queryset = Vote.objects.filter(property=Property.objects.get(pk=request.data['property']),
                                       voter=User.objects.get(pk=request.data['voter']))
        if queryset is not None:
            serializer = VoteSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response('No data', status=status.HTTP_204_NO_CONTENT)


class VoteUserFollowedPropertiesView(APIView):
    def post(self, request):
        propertiesFollowedbyUser = [i.property for i in Follow.objects.filter(follower=User.objects.get(pk=request.data['user']))]

        queryset = Vote.objects.filter(property__in=propertiesFollowedbyUser)
        if queryset is not None:
            serializer = VoteSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response('No data', status=status.HTTP_204_NO_CONTENT)


class VoteDetailsView(APIView):
    """
    Retrieve, update or delete an instance.
    """
    def get_object(self, pk):
        try:
            return Vote.objects.get(pk=pk)
        except Vote.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = VoteSerializer(instance)
        return Response(serializer.data)

    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        # CHECK IF ALREADY EXISTS
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = VoteSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response('Data erased', status=status.HTTP_204_NO_CONTENT)