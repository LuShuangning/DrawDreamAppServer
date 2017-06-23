from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt

from app_server.ModelForm.LoginRegistFrom import LoginFrom, RegistFrom
from .models import *


# 返回指定数据
@csrf_exempt
def index(request, op):
    data = swichdata(request, op)
    json = model2json(data)
    return HttpResponse(json, content_type="application/json; charset=utf-8")


# 登录
def login(request):
    lf = RegistFrom()
    if request.method == 'POST':
        uf = LoginFrom(request.POST)
        if uf.is_valid():
            # 获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 获取的表单数据与数据库进行比较
            print(username, password)
            user = Account.objects.filter(acco_num=username, acco_pwd=password)
            if user:
                return HttpResponseRedirect(request.POST.get('server', '/') or '/')
            else:
                return HttpResponseRedirect('/server/login/', status=302)
    else:
        uf = LoginFrom()
    return render(request, 'app_server/login.html', {'uf': uf, "lf": lf})


# 注册
def signup(request):
    if request.method == 'POST':
        lf = RegistFrom(request.POST)
        if lf.is_valid():
            # 获取表单用户密码
            email = lf.cleaned_data['email']
            username = lf.cleaned_data['username']
            password = lf.cleaned_data['password']
            re_password = lf.cleaned_data['re_password']
            if password != re_password:
                errors = "两次输入的密码不一致!"
                return render_to_response('app_server/login.html', {'errors': errors})
            # 获取的表单数据与数据库进行比较
            user = Account.objects.create(acco_num=username, acco_pwd=password)
            user = user.save()
            if user:
                return HttpResponseRedirect('/server/login/')
            else:
                return HttpResponseRedirect(request.POST.get('server', '/') or '/')
    else:
        uf = LoginFrom()
        lf = RegistFrom()
    return render(request, 'app_server/login.html', {'uf': uf, "lf": lf})


# 取字符串中两个符号之间的东东
def model2json(data):
    json = []
    for ech in data:
        _json = model_to_dict(ech)
        _json.setdefault("pk", str(ech.pk))
        json.append(_json)
    return json


categoryAction = {
    "Account": Account,
    "CommentReplay": CommentReplay,
    "NewsClassify": NewsClassify,
    "NewsDetail": NewsDetail,
    "UserCollect": UserCollect,
    "UserInfo": UserInfo
}


def swichdata(request, op=''):
    return categoryAction.get(op).objects.all()
