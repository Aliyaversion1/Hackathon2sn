from django.db import models

from account.models import MyUser


class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Discussion(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='discussions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='discussions')
    title = models.CharField(max_length=300)
    text = models.TextField()
    created = models.DateTimeField()

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to='discussions', blank=True, null=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='images')
