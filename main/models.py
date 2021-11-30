from django.db import models

from account.models import MyUser


class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.name}'


class Discussion(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='discussions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='discussions')
    title = models.CharField(max_length=300)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'


class Image(models.Model):
    image = models.ImageField(upload_to='discussions', blank=True, null=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='images')

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.built_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class Reply(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='replies')
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to='replies')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}: {self.body[:15]}'


class Comment(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comments')
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    moderator = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user} {self.comment}'


class Favorites(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='favorites')
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='favorites')
    favorites = models.BooleanField(default=False)

    def __str__(self):
        return {self.discussion}


class Rating(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='rating')
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='rating')
    rating = models.PositiveIntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.rating)


class Likes(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='likes')
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='likes')
    likes = models.BooleanField(default=False)

    def __str__(self):
        return {self.discussion}
