from django.contrib import admin
from .models import Post, Category, Tag

# Register your models here. 모델 만든거 admin에 넣어야함
admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Category, CategoryAdmin)

# 카테고리 모델의 name 필드에 값이 입력됐을 때 자동으로 slug가 만들어짐

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Tag, TagAdmin)

