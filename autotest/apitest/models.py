from django.db import models
from product.models import Product
class Apitest(models.Model):
    Product = models.ForeignKey('product.Product',on_delete=models.CASCADE,null=True)
    #关联产品ID，其中product是应用名，Product是应用的表名
    apitestname = models.CharField('流程接口名称',max_length=64)  #流程接口测试场景
    apitester = models.CharField('测试负责人',max_length=64,null=True)
    apitestdesc = models.CharField('描述',max_length=64,null=True)
    apitestresult = models.BooleanField('测试结果')
    create_time = models.DateTimeField('创建时间',auto_now=True)
    class Meta:
        verbose_name = '测试场景接口'
        verbose_name_plural = '流程场景接口'
    def __str__(self):
        return self.apitestname
class Apistep(models.Model):
    Apitest = models.ForeignKey('Apitest',on_delete=models.CASCADE)
    apiname = models.CharField('接口名称',max_length=200)
    apiurl = models.CharField('url地址',max_length=200)
    apiparamvalue = models.CharField('请求参数和值',max_length=800)
    REQUEST_METHOD = (('get','get'),('post','post'),('put','put'),('delete','delete'),('patch','patch'))
    apimethod = models.CharField(verbose_name='请求方法',choices = REQUEST_METHOD,default='get',max_length=200,null=True)
    apiresult = models.CharField('预期结果',max_length=200)
    apistatus = models.BooleanField('是否通过')
    create_time = models.DateTimeField('创建时间',auto_now=True)
    def __str__(self):
        return self.apiname

class Apis(models.Model):
    Product = models.ForeignKey('product.Product',on_delete=models.CASCADE,null=True)
    apiname = models.CharField('接口名称', max_length=200)
    apiurl = models.CharField('url地址', max_length=200)
    apiparamvalue = models.CharField('请求参数和值', max_length=800)
    REQUEST_METHOD = (('get', 'get'), ('post', 'post'), ('put', 'put'), ('delete', 'delete'), ('patch', 'patch'))
    apimethod = models.CharField(verbose_name='请求方法', choices=REQUEST_METHOD, default='get', max_length=200, null=True)
    apiresult = models.CharField('预期结果', max_length=200)
    apistatus = models.BooleanField('是否通过')
    create_time = models.DateTimeField('创建时间', auto_now=True)
    class Meta:
        verbose_name = '单一场景接口'
        verbose_name_plural = '单一场景接口'
    def __str__(self):
        return self.apiname
