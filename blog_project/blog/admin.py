from django.contrib import admin
from .models import *
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):



    class Media:
        js = (
            '/static/js/kindeditor-4.1.6/kindeditor-min.js',
            '/static/js/kindeditor-4.1.6/lang/zh_CN.js',
            '/static/js/kindeditor-4.1.6/config.js'
        )


admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Catagory)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(AD)