from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from slugify import slugify
# Create your models here.


class Group(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='user_groups', blank=True)
    title = models.CharField(max_length=250, unique=True)
    create_date = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    slug = models.SlugField(unique=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            suffix = 1
            while Group.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Post(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    text = models.TextField()







