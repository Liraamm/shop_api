from django.contrib import admin
from .models import *
# from django.db.models import Avg

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Article)
admin.site.register(Orders)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Like)


class RatingInline(admin.TabularInline):
    model = Rating

