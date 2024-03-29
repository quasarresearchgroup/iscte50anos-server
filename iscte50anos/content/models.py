from django.db import models
from topics.models import Topic


class Content(models.Model):
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=500, blank=True)
    topics = models.ManyToManyField(Topic, related_name='content')
    validated = models.BooleanField(null=False, default=False)
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
                    # ("text", "Text"),
                    # ("interview", "Interview")
                )
    )

    def __str__(self):
        return f'{self.id} - {self.title} - {self.type} - {self.link}'
