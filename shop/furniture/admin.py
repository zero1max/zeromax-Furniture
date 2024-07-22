from django.contrib import admin
from .models import Furniture, Category, Discount, News, WeHelp, Benefits
from django.utils.html import format_html

# Register your models here.
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'get_discount_price', 'quantity','category', 'created_at', 'updated_at', 'is_published', 'photo_tag']
    list_display_links = ['id', 'title']
    search_fields = ['title', 'description']
    list_editable = ['is_published', 'category']
    prepopulated_fields = {"slug": ('title',)}
    list_filter = ['is_published', 'category']

    def photo_tag(self, obj):
        if obj.photo:
            return format_html(f'<img src="{obj.photo.url}" width=80 height=auto>')
        else:
            return format_html('-')
    photo_tag.short_description = 'Photo'

    def get_discount_price(self, obj):
        return obj.get_discount_price()
    get_discount_price.short_description = 'Discount Price'


class WeHelpAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']


class BenefitsAdmin(admin.ModelAdmin):
    list_display = ['id', 'benefits']
    list_display_links = ['id', 'benefits']


class DiscountAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'owner', 'is_published', 'photo_tag']
    list_display_links = ['id', 'title']
    list_editable = ['is_published']

    def photo_tag(self, obj):
        if obj.photo:
            return format_html(f'<img src="{obj.photo.url}" width=80 height=auto>')
        else:
            return format_html('-')
    photo_tag.short_description = 'Photo'


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'is_published', 'photo_tag']
    list_editable = ['is_published']
    list_display_links = ['id', 'title']

    def photo_tag(self, obj):
        if obj.photo:
            return format_html(f'<img src="{obj.photo.url}" width=80 height=auto>')
        else:
            return format_html('-')
    photo_tag.short_description = 'Photo'

admin.site.register(Furniture, FurnitureAdmin)
admin.site.register(Category)
admin.site.register(WeHelp, WeHelpAdmin)
admin.site.register(Benefits,BenefitsAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(News, NewsAdmin)
admin.site.site_title = 'Furniture website'
admin.site.site_header = 'Furniture website'
