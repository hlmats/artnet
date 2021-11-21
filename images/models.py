from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Image(models.Model):
    STATUS_CHOICES = (('Renaissance', 'Renaissance'),
                      ('Mannerism', 'Mannerism'),
                      ('Baroque', 'Baroque'),
                      ('Classicism', 'Classicism'),
                      ('Romanticism', 'Romanticism'),
                      ('Impressionism', 'Impressionism'),
                      ('Expressionism', 'Expressionism'),
                      ('Avant-garde', 'Avant-garde'),
                      ('Other', 'Other'))
    ACTIVITY_CHOICES = (('Active', 'Active'),
                      ('Inactive', 'Inactive'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True,
                               db_index=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True)
    total_likes = models.PositiveIntegerField(db_index=True,
                                              default=0)
    style = models.CharField(max_length=200, choices=STATUS_CHOICES,
                              default='Other')
    activity = models.CharField(max_length=200, choices=ACTIVITY_CHOICES,
                              default='Active')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])



class Comment(models.Model):
    image = models.ForeignKey(Image,
                             on_delete=models.CASCADE,
                             related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='comment_created',
                             on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.user} on {self.image}'

