import requests
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import json
from django.http import Http404

from ..serializers import ChoiceSerializer
from ..models import Choice


class ChoiceView(APIView):
    def get(self, request):
        queryset = Choice.objects.all().order_by('order')
        if queryset is not None:
            serializer = ChoiceSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response('No data', status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        serializer = ChoiceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChoiceDetailsView(APIView):
    """
    Retrieve, update or delete an instance.
    """
    def get_object(self, pk):
        try:
            return Choice.objects.get(pk=pk)
        except Choice.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = ChoiceSerializer(instance)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChoiceSerializer(data=request.data)
        # CHECK IF ALREADY EXISTS
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = ChoiceSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response('Data erased', status=status.HTTP_204_NO_CONTENT)