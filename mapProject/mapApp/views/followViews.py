import requests
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import json
from django.http import Http404

from ..serializers import FollowSerializer, PropertySerializer
from ..models import Follow, Property, User

from .propertyViews import PropertyView


class FollowsView(APIView):
    def post(self, request):
        queryset = Follow.objects.filter(follower=request.data['follower'])
        if queryset is not None:
            serializer = FollowSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response('No data', status=status.HTTP_204_NO_CONTENT)


class FollowView(APIView):
    def get(self, request):
        queryset = Follow.objects.all().order_by('order')
        if queryset is not None:
            serializer = FollowSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response('No data', status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        followingAlreadyCreated = Follow.objects.filter(property=Property.objects.filter(osm_id=request.data['property']['osm_id'],
                                                                                         osm_type=request.data['property']['osm_type']).first(),
                                                         follower=User.objects.filter(pk=request.data['follower']).first()).first()
        if followingAlreadyCreated:
            return Response('Data erased', status=status.HTTP_204_NO_CONTENT)

        if (Property.objects.filter(osm_id=request.data['property']['osm_id'], osm_type=request.data['property']['osm_type'])):
            follower = User.objects.get(pk=request.data['follower'])
            property=Property.objects.filter(osm_id=request.data['property']['osm_id'], osm_type=request.data['property']['osm_type']).first()
            newFollow = Follow(follower=follower, property=property)
            newFollow.save()
            serializer = FollowSerializer(newFollow)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        serializerProperty = PropertySerializer(data=request.data['property'])
        if serializerProperty.is_valid(raise_exception=True):
            serializerProperty.save()
            follower = User.objects.get(pk=request.data['follower'])
            property = Property.objects.get(pk=serializerProperty.data['id'])
            newFollow = Follow(follower=follower, property=property)
            newFollow.save()
            serializer = FollowSerializer(newFollow)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class FollowViewDetailsView(APIView):
    """
    Retrieve, update or delete an instance.
    """
    def get_object(self, pk):
        try:
            return Follow.objects.get(pk=pk)
        except Follow.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = FollowSerializer(instance)
        return Response(serializer.data)

    def post(self, request):
        serializer = FollowSerializer(data=request.data)
        # CHECK IF ALREADY EXISTS
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = FollowSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response('Data erased', status=status.HTTP_204_NO_CONTENT)