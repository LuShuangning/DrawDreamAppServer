from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt

from app_server.ModelForm.LoginRegistFrom import LoginFrom, RegistFrom
from .models import *
import simplejson


# 返回指定数据
@csrf_exempt
def index(request, op):
    data = swichdata(request, op)
    json = model2json(data)
    return HttpResponse(json, content_type="application/json; charset=utf-8")


def result(request):
    test_dict = {}

    req = simplejson.loads(request.body)
    classify = req['classify']
    test_dict['classify'] = classify
    test_json = simplejson.dumps(test_dict).encode('utf-8').decode('unicode-escape')
    print('已获取json\n' + test_json)
    return HttpResponse(test_json, content_type="application/json; charset=utf-8")


def login(request):
    res = {}
    user_data = {}
    if request.method == 'POST':
        # 获取POST数据
        req = simplejson.loads(request.body)
        account = req['account']
        pwd = req['pwd']
        # 查询符合的记录
        user = Account.objects.get(acco_num=account, acco_pwd=pwd)
        print(str(user))
        if user:
            res['msg'] = '200'
            res['success'] = 'true'
            info = UserInfo.objects.get(usin_id=user.acco_id)
            user_data['id'] = 1
            user_data['user_id'] = str(info.usin_id_id)
            user_data['user_name'] = info.usin_name
            user_data['user_gender'] = str(info.usin_sex)
            user_data['user_phone'] = info.usin_phone
            user_data['user_email'] = info.usin_email
            user_data['user_sign'] = info.usin_sign
            res['data'] = user_data
            res_json = simplejson.dumps(res)
            print(res_json.encode('utf-8').decode('unicode-escape'))
        # 若记录不存在
        else:
            res['msg'] = '302'
            res['success'] = 'false'
            res['data'] = user_data
            res_json = simplejson.dumps(res).encode('utf-8').decode('unicode-escape')
            print(res_json)
    return HttpResponse(res_json, content_type="application/json; charset=utf-8")

# 登录
# def login(request):
#     lf = RegistFrom()
#     if request.method == 'POST':
#         uf = LoginFrom(request.POST)
#         if uf.is_valid():
#             # 获取表单用户密码
#             username = uf.cleaned_data['username']
#             password = uf.cleaned_data['password']
#             # 获取的表单数据与数据库进行比较
#             print(username, password)
#             user = Account.objects.filter(acco_num=username, acco_pwd=password)
#             if user:
#                 return HttpResponseRedirect(request.POST.get('server', '/') or '/')
#             else:
#                 return HttpResponseRedirect('/server/login/', status=302)
#     else:
#         uf = LoginFrom()
#     return render(request, 'app_server/login.html', {'uf': uf, "lf": lf})

    # return render(request, 'app_server/login.html')


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
