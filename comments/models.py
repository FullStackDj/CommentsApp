from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import os
import bleach

ALLOWED_TAGS = ['b', 'i', 'u', 'strong', 'em', 'code', 'a']

class UserInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    homepage = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        verbose_name = "User info"
        verbose_name_plural = "User info"

class Comment(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def save(self, *args, **kwargs):
        self.text = bleach.clean(self.text, tags=ALLOWED_TAGS, strip=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.name}: {self.text[:30]}"

def validate_file_extension(file):
    ext = os.path.splitext(file.name)[1].lower()
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.txt']
    if ext not in allowed_extensions:
        raise ValidationError('Unsupported file type. Allowed types: .jpg, .jpeg, .png, .gif, .txt')

def validate_file_size(file):
    max_size = 5 * 1024 * 1024
    if file.size > max_size:
        raise ValidationError('File size exceeds the 5MB limit.')

class Attachment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/', validators=[validate_file_extension, validate_file_size])

    def __str__(self):
        return f"Attachment for comment #{self.comment.id}"