from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import *
from .serializers import *


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DiscussionsViewSet(viewsets.ModelViewSet):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer

    @action(detail=False, methods=['Get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q)|
                                   Q(text__icontains=q))
        serializer = DiscussionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ImageView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = DiscussionImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}