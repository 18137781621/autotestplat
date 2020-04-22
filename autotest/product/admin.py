from django.contrib import admin
from product.models import Product
from apitest.models import Apis,Apitest
class ProductAdmin(admin.ModelAdmin):
    list_display = ['productname','productdesc','producter','create_time','id']
admin.site.register(Product) # 把产品模块注册到django admin后台并能显示

class ApisAdmin(admin.TabularInline):
    list_display = ['apiname','apiurl','apiparamvalue','apimethod','apiresult','apistatus','create_time','id','product']
    model =  Apis
    extra = 1

