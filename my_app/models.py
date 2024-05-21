from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=20, verbose_name="Categoriya nomi")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_list', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategorilayar"


class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name='Maqola Sarlavhasi')
    content = models.TextField(verbose_name='Maqola Matni')
    created_at = models.DateField(auto_now_add=True, verbose_name='Yaratilgan vaqti')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Yengilangan vaqti')
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='Maqola rasmi')
    watched = models.IntegerField(default=0, verbose_name="Korishlar soni")
    is_published = models.BooleanField(default=True, verbose_name='Yuklanganligi')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Kategoriya')
    author = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_details', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Maqola"
        verbose_name_plural = "Maqolalar"
        ordering = ['-created_at']


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
