from django.contrib import admin
from .models import GanGeneratedModel, Voxel
from django.utils.html import format_html

class GanGeneratedModelAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))

    image_tag.short_description = 'Generated image'
    list_display = ['name', 'generated_Img']


admin.site.register(GanGeneratedModel, GanGeneratedModelAdmin)

class VoxelAdmin(admin.ModelAdmin):

    list_display = ['model', 'data']

admin.site.register(Voxel)