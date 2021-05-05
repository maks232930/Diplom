from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Tag,
    Comment,
    Post,
    Category
)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    list_display_links = ('title', 'slug',)
    prepopulated_fields = {'slug': ('title',)}


class PostFormAdmin(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostFormAdmin
    list_display = (
        'author', 'title', 'category', 'published_date', 'is_published', 'views', 'get_photo')
    list_display_links = (
        'author', 'title', 'category', 'published_date', 'views', 'get_photo')
    list_filter = ('category', 'author')
    list_editable = ('is_published',)
    search_fields = ('title', 'content')
    readonly_fields = ('get_photo', 'views', 'author')
    prepopulated_fields = {'slug': ('title',)}
    save_as = True
    save_on_top = True

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')

    get_photo.short_description = 'Фото'

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content', 'published_date', 'is_published')
    list_display_links = ('user', 'post', 'content', 'published_date')
    list_filter = ('post',)
    search_fields = ('content',)
    list_editable = ('is_published',)
    save_as = True
    save_on_top = True


admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
