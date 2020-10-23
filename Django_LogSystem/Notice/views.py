from django.shortcuts import render,redirect
from Report.models import ReportsInfo
from Login.models import LoginUser

# Create your views here.

def CommentNoticeList(request):
    isactive = ''
    user = request.session['user_name']
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    notices = LoginUser.objects.get(username=user).notifications.unread()
    return render(request, 'notice/list.html', locals())


def CommentNoticeUpdate(request):
    isactive = ''
    user = request.session['user_name']
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    notice_id = request.GET.get('notice_id')
    if notice_id:
        report = ReportsInfo.objects.get(ReportNumber=request.GET.get('ReportNumber'))
    else:
        LoginUser.objects.get(username=user).notifications.mark_all_as_read()
        return render(request, 'notice/list.html', locals())

