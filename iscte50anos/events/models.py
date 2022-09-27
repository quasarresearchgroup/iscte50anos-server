from django.db import models

from topics.models import Topic

from content.models import Content


class Event(models.Model):
    title = models.CharField(max_length=300)
    topics = models.ManyToManyField(Topic, related_name='events')
    content = models.ManyToManyField(Content, related_name='events')

    date = models.DateField(null=True, blank=True)

    scope = models.CharField(
        max_length=12,
        choices=(
            ("iscte", "Iscte"),
            ("portugal", "Portugal"),
            ("world", "World"),
        ),
        default="iscte"
    )

    def __str__(self):
        return f'{self.id} - {self.date} - {self.title} - {self.scope}'

    def num_content(self):
        return self.content.all().count()

    class Meta:
        ordering = ['date']
