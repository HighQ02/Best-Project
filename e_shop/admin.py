from django.contrib import admin
from .models import *

# Register your models here.
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_category', 'price_in_kzt', 'price_in_usd')
    ordering = ('name', 'id')
    list_filter = ('category', 'price')
    search_fields = ('name', 'description')
    fields = ('name', 'description', 'price', 'image', 'category')

    def price_in_kzt(self, obj):
        return str(obj.price) + '₸'

    def price_in_usd(self, obj):
        return str(obj.price/500) + '$'

    def product_category(self, obj):
        from django.utils.html import format_html
        return format_html('<b>' + obj.category.name + '</b>')
        

admin.site.register(Category)
admin.site.register(Product, ProductsAdmin)
admin.site.register(Profile)
admin.site.register(BoughtProducts)
admin.site.register(Basket)
admin.site.register(Review)
admin.site.register(Reply)
admin.site.register(Conversation)
admin.site.register(ConversationMessage)