from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    rating_auth = models.IntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Is it need NULL = True??

    def __str__(self):
        return f'{self.user.username}'

    def update_rating(self):
        postRat = self.post_set.all().aggregate(postRating=Sum('rating_post'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.user.comment_set.all().aggregate(commentRating=Sum('rating_com'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.rating_auth = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.category}'


# article = 'AR'
# new = 'NW'


class Post(models.Model):
    article = 'AR'
    new = 'NW'
    TYPES = [
        (article, 'Статья'),
        (new, 'Новость')
    ]
    type = models.CharField(max_length=2, choices=TYPES, default=article)
    time_post = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=122)
    text_post = models.TextField()
    rating_post = models.IntegerField(default=0)

    authors = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return self.text_post[0:123] + '...'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'

    #def __str__(self):
    #    return f'{self.name.title()}: {self.text_post}, {self.type}, {self.rating_post}, {self.time_post}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text_com = models.TextField()
    time_com = models.DateTimeField(auto_now_add=True)
    rating_com = models.IntegerField(default=0)

    posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating_com += 1
        self.save()

    def dislike(self):
        self.rating_com -= 1
        self.save()
# Create your models here.
