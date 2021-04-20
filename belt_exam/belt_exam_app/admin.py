from django.contrib import admin

# Register your models here.
from .models import User, Thoughts, Likes

admin.site.register(User)
admin.site.register(Thoughts)
admin.site.register(Likes)