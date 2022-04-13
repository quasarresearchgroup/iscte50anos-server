from django.db import models
from topics.models import Topic


class Content(models.Model):
    title = models.CharField(max_length=50)
    link = models.CharField(max_length=100, blank=True)
    topics = models.ManyToManyField(Topic, related_name='content')

    # date = models.DateField(null=True, blank=True)

    type = models.CharField(
        max_length=12,
        choices=(
                    ("document", "Document"),
                    ("web_page", "Web page"),
                    ("image", "Image"),
                    ("audio", "Audio"),
                    ("video", "Video"),
                    ("social_media", "Social media")
                )
    )

    def __str__(self):
        return self.title
