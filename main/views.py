from datetime import timedelta

from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import *
from .permissions import IsTheDiscussionOwner
from .serializers import *


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DiscussionsViewSet(viewsets.ModelViewSet):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        queryset = super().get_queryset()
        days_count = int(self.request.query_params.get('day', 0))
        if days_count > 0:
            start_date = timezone.now() - timedelta(days=days_count)
            queryset = queryset.filter(created__gte=start_date)
        return queryset

    def get_permissions(self):
        if self.action in ['update', 'partial-update', 'destroy']:
            permissions = [IsTheDiscussionOwner]
        else:
            permissions = [IsAuthenticated, ]
        return [permission() for permission in permissions]

    @action(detail=False, methods=['get'])
    def own(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = DiscussionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def search(self, request, pk=None):
        query = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=query) |
                                   Q(text__icontains=query))
        serializer = DiscussionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)











    @action(detail=False, methods=['get'])
    def favorites(self, request):
        queryset = Favorites.objects.all()
        queryset = queryset.filter(user=request.user)
        serializer = FavoritesSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, ])
    def favorite(self, request, pk=None):
        discussion = self.get_object()
        obj, created = Favorites.objects.get_or_create(user=request.user, discussion=discussion, )
        if not created:
            obj.favorites = not obj.favorites
            obj.save()
        favorites = 'You add this discussion in favorites' if obj.favorites else 'You removed this discussion from favorites'

        return Response('Successfully: {} !'.format(favorites), status=status.HTTP_200_OK)


class ImageView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = DiscussionImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated, ]


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated, ]


class LikesViewSet(viewsets.ModelViewSet):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    permission_classes = [IsAuthenticated, ]


