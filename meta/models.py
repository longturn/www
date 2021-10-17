from django.db import models
from django.utils import timezone
from datetime import timedelta

class Server(models.Model):
    url = models.URLField(primary_key=True)
    id = models.SlugField()
    message = models.CharField(max_length=1024)
    patches = models.CharField(max_length=256)
    capability = models.CharField(max_length=256)
    version = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    available = models.IntegerField()
    humans = models.IntegerField()
    last_seen = models.DateTimeField(default=timezone.now)

    @staticmethod
    def remove_old():
        """Remove servers with no news for 10 minutes. Normal servers report
        every 3 minutes."""
        Server.objects \
            .filter(last_seen__lt = timezone.now() - timedelta(minutes=10)) \
            .delete()

    def json(self):
        return dict(
            url = self.url,
            id = self.id,
            message = self.message,
            patches = self.patches,
            capability = self.capability,
            version = self.version,
            state = self.state,
            available = self.available,
            humans = self.humans,
        )
