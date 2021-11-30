from django.contrib import admin

from .models import *


class DiscussionImageInLine(admin.TabularInline):
    model = Image
    max_num = 10


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    inlines = [DiscussionImageInLine, ]


admin.site.register(Category)
admin.site.register(Reply)
admin.site.register(Comment)
