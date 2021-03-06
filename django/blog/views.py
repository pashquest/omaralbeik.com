from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import permissions

from . import models, serializers
import tags


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    # return only published items
    queryset = models.Post.objects.filter(published=True)
    serializer_class = serializers.PostSerializer

    # detail route to return post tags
    # .../blog/posts/[post_id]/tags
    @detail_route(methods=['get'])
    def tags(self, request, pk=None):
        post = self.get_object()
        serializer = tags.serializers.TagSerializer(post.tags, many=True)
        return Response(serializer.data)

    # list route to return latest blog posts
    # .../blog/posts/latest
    @list_route()
    def latest(self, request):
        latest_posts = models.Post.objects.filter(published=True)[:2]
        serializer = self.get_serializer(latest_posts, many=True)
        return Response(serializer.data)
