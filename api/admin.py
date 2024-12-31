from django.contrib import admin
from .models import CMDB

# Register your models here.
admin.site.site_header = "CMDB"
admin.site.index_title = "CMDB后台"


class CMDBAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'data')


admin.site.register(CMDB, CMDBAdmin)
