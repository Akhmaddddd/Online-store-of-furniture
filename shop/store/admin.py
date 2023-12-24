from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


# Register your models here.

class ColorAdmin(admin.TabularInline):
    fk_name = 'product'
    model = Color
    extra = 1


class GalleryAdmin(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent','get_count_products')
    prepopulated_fields = {'slug': ('title',)}

    def get_count_products(self,obj):
        if obj.products:
            return str(len(obj.products.all()))
        else:
            return '0'

    get_count_products.short_description='Количество товара'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'quantity', 'price', 'created_at', 'length','width','height', 'get_photo')
    list_editable = ('price', 'quantity', 'length','width','height', )
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'price', 'category')
    inlines = [GalleryAdmin,ColorAdmin]


    def get_photo(self,obj):
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="75">')
            except:
                return '-'

        else:
            return '-'

    get_photo.short_description='Картинка'



admin.site.register(Gallery)
admin.site.register(Color)
admin.site.register(FavoriteProduct)
admin.site.register(MailCustomer)

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(ShippingAddress)
admin.site.register(City)
admin.site.register(Profile)
admin.site.register(SaveOrder)
admin.site.register(SaveOrderProducts)
