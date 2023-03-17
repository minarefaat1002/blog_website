from django.contrib import admin
from . import models


admin.site.register(models.Blog) 
admin.site.register(models.Category)
admin.site.register(models.Comment)
# @admin.register(models.Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ("post","created")
#     list_filter = ("created")
#     search_fields = ("post","content")