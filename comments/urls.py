from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import CommentViewSet, CommentCreateAPIView, comment_page
from .views import CommentPreviewAPIView


router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = router.urls + [
    path('create/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('preview/', CommentPreviewAPIView.as_view(), name='comment-preview'),
    path('page/', comment_page, name='comment-test'),
]