from django import forms
from django.forms import ModelForm
from . import models


class NewReport(ModelForm):
    class Meta:
        model = models.ReportsInfo
        fields = ['ReportDate', 'ReportWork', 'ReportProblem', 'ReportPlan']
#    PreviosReportData = forms.CharField(label="上次报告时间", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
#    PreviosReport = forms.CharField(label="拟定计划", max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ReportDate = forms.CharField(label="报告时间", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
#    ReportWork = forms.TextField(label="当前工作", max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
#    ReportProblem = forms.TextField(label="当前困难", max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
#    ReportPlan = forms.TextField(label="下一步计划", max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))

class CommentForm(ModelForm):
    class Meta:
        model = models.Comments
        fields = ['ReportComment']
#    ReportComment = forms.CharField(label="评论", max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
