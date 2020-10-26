from django.db import models

# Create your models here.

class ReportsInfo(models.Model):
    ReportNumber = models.AutoField(primary_key=True)
    ReportUser = models.CharField(max_length=10)
#    ReportEmail = models.CharField(max_length=256)
    ReportDate = models.DateTimeField('日志时间', null=True)
    ReportWork = models.TextField(verbose_name='当前工作', blank=True)
    ReportProblem = models.TextField(verbose_name='遇到的困难',blank=True)
    ReportPlan = models.TextField(verbose_name='当前计划', blank=True)

class Comments(models.Model):
    TargetReport = models.ForeignKey(ReportsInfo,on_delete=models.CASCADE)
    ReportComment = models.TextField(verbose_name='评论', blank=True)
