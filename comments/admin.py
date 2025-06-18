from django.contrib import admin
from .models import UserInfo, Comment, Attachment

admin.site.register(UserInfo)
admin.site.register(Comment)
admin.site.register(Attachment)