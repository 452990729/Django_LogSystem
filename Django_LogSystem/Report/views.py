import os
import time
import json
from django.shortcuts import render,redirect,HttpResponse
from . import models
from .forms import NewReport,CommentForm
from Login.models import LoginUser
from django.utils import timezone
from notifications.signals import notify
# Create your views here.

def CreateNew(request):
    isactive = 'new'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    user = request.session['user_name']
    list_ob = models.ReportsInfo.objects.order_by('ReportDate').filter(ReportUser=user)
    if len(list_ob) > 0:
        ob = list_ob[0]
        PreviesDate = ob.ReportDate.strftime('%Y-%m-%d %H:%M:%S')
        PreviesPlan = ob.ReportPlan
    else:
        PreviesDate = '无'
        PreviesPlan = '无'
    if request.method == "POST":
        NewReportForm = NewReport(request.POST)
        message = "please check in the content!"
        if NewReportForm.is_valid():
            ReportDate = NewReportForm.cleaned_data['ReportDate']
            ReportWork = NewReportForm.cleaned_data['ReportWork']
            ReportProblem = NewReportForm.cleaned_data['ReportProblem']
            ReportPlan = NewReportForm.cleaned_data['ReportPlan']
            new_project = models.ReportsInfo()
            new_project.ReportUser = user
            new_project.ReportDate = ReportDate
            new_project.ReportWork = ReportWork
            new_project.ReportProblem = ReportProblem
            new_project.ReportPlan = ReportPlan
            new_project.save()
            notify.send(
                LoginUser.objects.get(username=user),
                recipient=LoginUser.objects.get(username=LoginUser.objects.get(username=user).info_right),
                verb='提交了日志',
                target=new_project,
            )
            return redirect('/Report/loginfor/')
        return render(request, 'Report/new.html', locals())
    NewReportForm = NewReport()
    return render(request, 'Report/new.html', locals())

def Index(request):
    isactive = 'loginfor'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    data_list = []
    user = request.session['user_name']
    for data_info in models.ReportsInfo.objects.filter(ReportUser=user):
        data_list.append({
            '日志编号':data_info.ReportNumber,
            '日志记录人':data_info.ReportUser,
            '日志日期':data_info.ReportDate.strftime('%Y-%m-%d %H:%M:%S'),
        })
    data_dic = {}
    data_dic['userlog'] = data_list
    return render(request, 'Report/index.html', data_dic)

def Detail(request, project):
    isactive = 'loginfor'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    Project_model = models.ReportsInfo.objects.get(ReportNumber=project)
    comment_modle = models.Comments.objects.filter(TargetReport=project)
    com = ''
    for ml in comment_modle:
        com += '----'+ml.ReportComment
    ReportUser = Project_model.ReportUser
    ReportDate = Project_model.ReportDate.strftime('%Y-%m-%d %H:%M:%S')
    ReportWork = Project_model.ReportWork
    ReportProblem = Project_model.ReportProblem
    ReportPlan = Project_model.ReportPlan
    Com = com
    return render(request, 'Report/detail.html', locals())

def Del(request, project):
    isactive = 'loginfor'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    Project_model = models.ReportsInfo.objects.get(ReportNumber=project)
    Project_model.delete()
    return Index(request)

def SubAlin(request):
    isactive = 'sub'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    user = request.session['user_name']
    data_list = []
    list_sub = LoginUser.objects.filter(info_right=user)
    for sub in list_sub:
        reports = models.ReportsInfo.objects.filter(ReportUser=sub.username)
        for data_info in reports:
            data_list.append({
                '日志编号':data_info.ReportNumber,
                '日志记录人':data_info.ReportUser,
                '日志日期':data_info.ReportDate.strftime('%Y-%m-%d %H:%M:%S'),
            })
    data_dic = {}
    data_dic['userlog'] = data_list
    return render(request, 'Report/sub.html', data_dic)

def SubSingleDetail(request, project):
    isactive = 'sub'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    Project_model = models.ReportsInfo.objects.get(ReportNumber=project)
    comment_modle = models.Comments.objects.filter(TargetReport=project)
    com = ''
    for ml in comment_modle:
        com += '----'+ml.ReportComment
    ReportUser = Project_model.ReportUser
    ReportDate = Project_model.ReportDate.strftime('%Y-%m-%d %H:%M:%S')
    ReportWork = Project_model.ReportWork
    ReportProblem = Project_model.ReportProblem
    ReportPlan = Project_model.ReportPlan
    Com = com
    return render(request, 'Report/subsingledetail.html', locals())

def SubComment(request, project):
    isactive = 'sub'
    user = request.session['user_name']
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    Project_model = models.ReportsInfo.objects.get(ReportNumber=project)
    comment_modle = models.Comments.objects.filter(TargetReport=project)
    com = ''
    for ml in comment_modle:
        com += '----'+ml.ReportComment
    ReportUser = Project_model.ReportUser
    ReportDate = Project_model.ReportDate.strftime('%Y-%m-%d %H:%M:%S')
    ReportWork = Project_model.ReportWork
    ReportProblem = Project_model.ReportProblem
    ReportPlan = Project_model.ReportPlan
    Com = com
    SubCommentForm = CommentForm()
    if request.method == "POST":
        SubCommentForm = CommentForm(request.POST)
        message = "please check in the content!"
        if SubCommentForm.is_valid():
            ReportComment = SubCommentForm.cleaned_data['ReportComment']
            models.Comments.objects.create(TargetReport=Project_model, ReportComment=ReportComment)
            notify.send(
                LoginUser.objects.get(username=user),
                recipient=LoginUser.objects.get(username=ReportUser),
                verb='评论了日志',
                target=Project_model,
            )
            return render(request, 'Report/subsingledetail.html', locals())
        return render(request, 'Report/comment.html', locals())
    return render(request, 'Report/comment.html', locals())

def SubDetail(request, number):
    isactive = 'sub'
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    user = request.session['user_name']
    list_sub = LoginUser.objects.filter(info_right=user)
    out = ''
    now = timezone.now()
    for sub in list_sub:
        out += '<h2 class="text-left">{}</h2>'.format(sub.username)
        reports = models.ReportsInfo.objects.filter(ReportUser=sub.username)
        for data_info in reports:
            if (now-data_info.ReportDate).days<int(number):
                out += '<table class="table table-hover"><thead><tr><th>类别</th><th>内容</th></tr></thead>'
                out += '<tbody><tr><td>日志日期</td><td>{}</td></tr>'.format(data_info.ReportDate.strftime('%Y-%m-%d %H:%M:%S'))
                out += '<tbody><tr><td>当前工作</td><td>{}</td></tr>'.format(data_info.ReportWork)
                out += '<tbody><tr><td>当前困难</td><td>{}</td></tr>'.format(data_info.ReportProblem)
                out += '<tbody><tr><td>下一步计划</td><td>{}</td></tr>'.format(data_info.ReportPlan)
                out += '</tbody></table><br />'
        out += '<br /><br /><br /><br />'
    return render(request, 'Report/subdetail.html', locals())

def Upload(request):
    file_obj = request.FILES.get('UploadFile')
    file_type = request.GET.get('dir')
    file_obj.name = '{}{}'.format(time.time(), file_obj.name)
    file_dir = 'media{}{}'.format(os.sep, file_type)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_path = os.path.join("media", file_type, file_obj.name)
    with open(file_path, 'wb') as f:
        for line in file_obj:
            f.write(line)
    print(file_type)
    print(file_obj.name)
    dic = {'error': 0, 'url': '/media/{}/{}'.format(file_type, file_obj.name), 'message': '出现内部错误'}
    return HttpResponse(json.dumps(dic))

