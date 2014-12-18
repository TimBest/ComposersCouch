from django.contrib import admin
from photos.models import Image
from sorl.thumbnail.admin import AdminInlineImageMixin
from django.conf import settings

class InlineImageAdmin(AdminInlineImageMixin, admin.TabularInline):
    model = Image
    fieldsets = ((None, {'fields': ['image', 'user', 'title', 'order', 'tags']}),)
    raw_id_fields = ('user', )
    extra = 0


class ImageAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['user', 'title', 'image', 'description', 'order', 'tags']}),)
    list_display = ('admin_thumbnail', 'user', 'order', 'title')
    raw_id_fields = ('user', )

IMAGE_MODEL = getattr(settings, 'PHOTOS_IMAGE_MODEL', None)
if not IMAGE_MODEL:
    admin.site.register(Image, ImageAdmin)

