from django.contrib import admin
from .models import Post, Author, Comment, PostCategory, Category

admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(PostCategory)
admin.site.register(Category)
# Register your models here.
