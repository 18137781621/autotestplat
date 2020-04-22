from django.contrib import admin
from bug.models import Bug

class BugAdmin(admin.ModelAdmin):
    list_display = ['bugname','bugdetail','bugstatus','buglevel','bugcreater','bugassign','create_time','id']
admin.site.register(Bug)
