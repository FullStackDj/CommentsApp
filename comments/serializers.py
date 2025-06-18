from rest_framework import serializers
from .models import UserInfo, Comment, Attachment
from captcha.fields import CaptchaField

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'file']

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['id', 'name', 'email', 'homepage']

class CommentSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()
    attachments = AttachmentSerializer(many=True, read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at', 'parent', 'attachments', 'replies']

    def get_replies(self, obj):
        qs = obj.replies.all()
        return CommentSerializer(qs, many=True).data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user, created = UserInfo.objects.get_or_create(email=user_data['email'], defaults=user_data)
        comment = Comment.objects.create(user=user, **validated_data)
        return comment

class CommentCreateSerializer(serializers.ModelSerializer):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ['user', 'text', 'parent', 'captcha']

    def validate(self, data):
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user, _ = UserInfo.objects.get_or_create(email=user_data['email'], defaults=user_data)
        comment = Comment.objects.create(user=user, **validated_data)
        return comment