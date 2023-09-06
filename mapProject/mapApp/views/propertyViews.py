import requests
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import json
from django.http import JsonResponse
from django.http import Http404
from decimal import Decimal

import osmnx as ox

from ..serializers import PropertySerializer
from ..models import Property

from ..utils import distanceCoordinates

class PropertyView(APIView):
    def get(self, request):
        queryset = Property.objects.all()
        if queryset is not None:
            serializer = PropertySerializer(queryset, many=True)
            return Response(serializer.data)
        return Response('No data', status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        serializer = PropertySerializer(data=request.data)
        propertyAlreadyCreated = Property.objects.filter(osm_id=request.data['osm_id'], osm_type=request.data['osm_type']).first()
        if propertyAlreadyCreated:
            serializer = PropertySerializer(propertyAlreadyCreated)
            return Response(serializer.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            propertyCreated = Property.objects.get(pk=serializer.data['id'])
            if propertyCreated.name is None or propertyCreated.name == '':
                propertyCreated.name = propertyCreated.display_name
                propertyCreated.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PropertyCheckView(APIView):
    def post(self, request):
        serializer = PropertySerializer(data=request.data)
        propertyAlreadyCreated = Property.objects.filter(osm_id=request.data['osm_id'],
                                                         osm_type=request.data['osm_type']).first()
        if propertyAlreadyCreated:
            serializer = PropertySerializer(propertyAlreadyCreated)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('No data', status=status.HTTP_204_NO_CONTENT)


class PropertyDetailsView(APIView):
    """
    Retrieve, update or delete an instance.
    """
    def get_object(self, pk):
        try:
            return Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = PropertySerializer(instance)
        return Response(serializer.data)

    def post(self, request):
        serializer = PropertySerializer(data=request.data)
        # CHECK IF ALREADY EXISTS
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = PropertySerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response('Data erased', status=status.HTTP_204_NO_CONTENT)


class PropertyQueryLocationView(APIView):
    def post(self, request):
        coordinatesLatRequested = Decimal(request.data['itemObject']['latitude'])
        coordinatesLonRequested = Decimal(request.data['itemObject']['longitude'])
        allProperties = Property.objects.filter(with_suggestions=True)
        propertiesInDistance = []
        for i in allProperties:
                valueDistance = distanceCoordinates.get_distance(coordinatesLatRequested, coordinatesLonRequested,
                                                             i.lat, i.lon)
                if (valueDistance <= 10):
                    propertiesInDistance.append(i)
        if len(propertiesInDistance) > 0:
            serializer = PropertySerializer(propertiesInDistance, many=True)
            return Response(serializer.data)
        return Response('No data', status=status.HTTP_204_NO_CONTENT)


class PropertyQueryLocationViewNotInDBAll(APIView):
    def post(self, request):
        print(request.data['itemObjectSearchAround']['coordinates'])
        coordinatesLatRequested = Decimal(request.data['itemObjectSearchAround']['coordinates']['lat'])
        coordinatesLonRequested = Decimal(request.data['itemObjectSearchAround']['coordinates']['lon'])
        allProperties = request.data['itemObjectSearchAround']['properties']
        propertiesInDistance = []
        for i in allProperties:
            print(i)
            valueDistance = distanceCoordinates.get_distance(coordinatesLatRequested, coordinatesLonRequested,
                                                             i['lat'], i['lon'])
            if (valueDistance <= 10):
                    propertiesInDistance.append(i)
        if len(propertiesInDistance) > 0:
            # serializer = PropertySerializer(propertiesInDistance, many=True)
            # return Response(serializer.data)
            return JsonResponse(propertiesInDistance, safe=False)
        return Response('No data', status=status.HTTP_204_NO_CONTENT)


class PropertyQueryLocationDBView(APIView):
    def post(self, request):
        propertiesToReturn = []
        for i in request.data['itemObject']:
            if (Property.objects.filter(osm_id=i['osm_id'],
                                                     osm_type=i['osm_type']).first()):
                propertyToAdd = Property.objects.filter(osm_id=i['osm_id'],
                                                     osm_type=i['osm_type']).first()
                serializer = PropertySerializer(propertyToAdd)
                propertiesToReturn.append(serializer.data)
            else:
                propertiesToReturn.append((i))
        return JsonResponse(propertiesToReturn, safe=False)


# osmnx.features.features_from_bbox(north, south, east, west, tags)
# osmnx.features.features_from_point(center_point, tags, dist=1000)
# https://osmnx.readthedocs.io/en/stable/user-reference.html

class PropertyQueryLocationAroundView(APIView):
    def post(self, request):
        infoEx = ox.features.features_from_point((request.data['itemObject']['lat'],request.data['itemObject']['lng']),
                                                 tags={"amenity": True}, dist=100)
        return JsonResponse(infoEx.to_json(), safe=False)
