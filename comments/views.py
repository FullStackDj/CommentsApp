from rest_framework import mixins, viewsets, filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import render_comment_preview


class CommentViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = []
    ordering_fields = ['user__name', 'user__email', 'created_at']
    ordering = ['-created_at']

class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        comment = serializer.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "comments",
            {
                "type": "comment_message",
                "message": f"New comment from {comment.user.name}: {comment.text[:50]}"
            }
        )

class CommentPreviewAPIView(APIView):
    def post(self, request):
        text = request.data.get("text", "")
        preview = render_comment_preview(text)
        return Response({"preview": preview}, status=status.HTTP_200_OK)


def comment_page(request):
    return render(request, 'comments/index.html')