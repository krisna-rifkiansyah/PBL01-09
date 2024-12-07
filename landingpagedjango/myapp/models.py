from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from django.utils.timezone import now

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {self.text[:30]}'
    
class LogEntry(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    key = models.CharField(max_length=50)
    txt = models.CharField(max_length=255)
    session = models.CharField(max_length=50)
    ipaddr = models.GenericIPAddressField()
    app = models.CharField(max_length=50, default='PBL01LOGS')
    time = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.key} - {self.txt} - {self.session}"