from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Category, Images, Product, Comment


# Register your models here.

class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    # prepopulated_fields = {'slug': ('title',)}
    # inlines = [CategoryLangInline]
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                                                Product,
                                                'category',
                                                'products_count',
                                                cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count

    related_products_count.short_description = 'محصولات مرتبط (برای این دسته خاص)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count

    related_products_cumulative_count.short_description = 'محصولات مرتبط (در درخت)'



# this class for show Products on the Admin Panel
# ____________________________________________________________
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'image_tag']
    list_filter = ['category', ]
    readonly_fields = ['image_tag']
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ('title',)}

# this class for show the Images on the Admin panel
# ___________________________________________________________
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'image']


#this class for the information on the userAdmin
#_______________________________________________________________

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject','comment','status','create_at']
    list_filter = ['status']
    readonly_fields = ['subject','comment','ip','user','product','rate']


admin.site.register(Comment,CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images, ImageAdmin)