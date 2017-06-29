from datetime import date, datetime
import json
from uuid import UUID

import simplejson
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt

from app_server.ModelForm.LoginRegistFrom import LoginFrom, RegistFrom
from .models import *


# 返回指定数据
# @csrf_exempt
# def index(request, op):
#     data = swichdata(request, op)
#     _json = model2json(data)
#     # res_json = json.dumps(_json).encode('utf-8').decode('unicode-escape')
#     return HttpResponse(_json, content_type="application/json; charset=utf-8")

@csrf_exempt
def index(request):
    res = {}
    req = json.loads(request.body)
    if req:
        print("已获取POST请求")
    res_list = NewsDetail.objects.all()
    if res_list.count() == 0:
        res['msg'] = '404'
        res['success'] = 'false'
    else:
        res['msg'] = '200'
        res['success'] = 'true'

    _json = model2json(res_list)
    res['data'] = _json
    # res_json = json.dumps(res).encode('utf-8').decode('unicode-escape')
    res_json = json.dumps(res, ensure_ascii=False, default=__default).encode("utf-8")
    return HttpResponse(res_json, content_type="application/json; charset=utf-8")


def result(request):
    test_dict = {}

    req = json.loads(request.body)
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
        try:
            user = Account.objects.get(acco_num=account)
            if user.acco_pwd == pwd:
                print(str(user))
                res['msg'] = '200'
                res['success'] = 'true'
                info = UserInfo.objects.get(usin_id=user.acco_id)
                user_data['user_id'] = str(info.usin_id_id)
                user_data['user_name'] = info.usin_name
                user_data['user_gender'] = str(info.usin_sex)
                user_data['user_phone'] = info.usin_phone
                user_data['user_email'] = info.usin_email
                user_data['user_sign'] = info.usin_sign
                # user_data = model2json(info)
                res['data'] = user_data
            # 密码错误
            else:
                res['msg'] = '405'
                res['success'] = 'false'
                res['data'] = user_data
        # 用户不存在
        except Account.DoesNotExist:
            res['msg'] = '404'
            res['success'] = 'false'
            res['data'] = user_data

    res_json = json.dumps(res).encode('utf-8').decode('unicode-escape')
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
# def signup(request):
#     if request.method == 'POST':
#         lf = RegistFrom(request.POST)
#         if lf.is_valid():
#             # 获取表单用户密码
#             email = lf.cleaned_data['email']
#             username = lf.cleaned_data['username']
#             password = lf.cleaned_data['password']
#             re_password = lf.cleaned_data['re_password']
#             if password != re_password:
#                 errors = "两次输入的密码不一致!"
#                 return render_to_response('app_server/login.html', {'errors': errors})
#             # 获取的表单数据与数据库进行比较
#             user = Account.objects.create(acco_num=username, acco_pwd=password)
#             user = user.save()
#             if user:
#                 return HttpResponseRedirect('/server/login/')
#             else:
#                 return HttpResponseRedirect(request.POST.get('server', '/') or '/')
#     else:
#         uf = LoginFrom()
#         lf = RegistFrom()
#     return render(request, 'app_server/login.html', {'uf': uf, "lf": lf})

def user_info(request):
    res = {}
    # 获取POST数据
    req = simplejson.loads(request.body)

    user_id = int(req['user_id'])
    userInfo = UserInfo.objects.get(usin_id_id=user_id)
    print(req['user_email'])
    if req['user_gender']:
        gender = True
    else:
        gender = False
    try:
        userInfo.usin_name = req['user_name']
        userInfo.usin_sex = gender
        userInfo.usin_sign = req['user_sign']
        userInfo.usin_email = req['user_email']
        userInfo.save()

        res['msg'] = '200'
        res['success'] = 'true'
    except:
        res['msg'] = '302'
        res['success'] = 'false'
    finally:
        res_json = json.dumps(res).encode('utf-8').decode('unicode-escape')
        print(res_json)
    return HttpResponse(res_json, content_type="application/json; charset=utf-8")


def comment(request):
    res = {}
    comment = []
    # 获取POST数据
    # req = simplejson.loads(request.body)
    # core_nede_id = req['news_id']
    core_nede_id = '068cf57b92f846bc9204fed56f30b8e8'
    try:
        comment_list = CommentReplay.objects.filter(core_nede_id_id=core_nede_id)
        # _json = model2json(comment_list)
        # 最笨的方法，在循环里面再写查询，先把自己鄙视一番
        for m in comment_list:
            comment_data = {}
            n = UserInfo.objects.get(usin_id_id=m.core_acco_id_id)
            comment_data['content'] = m.core_content
            comment_data['name'] = n.usin_name
            comment_data['core_date'] = str(m.core_date)
            comment_data['id'] = str(m.id)
            comment.append(comment_data)
    # 若评论为空
    except CommentReplay.DoesNotExist:
        res['msg'] = '302'
        res['success'] = 'false'
        res['data'] = ''
    finally:
        res['data'] = comment
        res_json = json.dumps(res).encode('utf-8').decode('unicode-escape')

    return HttpResponse(res_json, content_type="application/json; charset=utf-8")


def deliver_comment(request):
    res = {}
    content = res['content']
    user_id = res['user_id']
    news_id = res['news_id']
    CommentReplay(core_acco_id_id=user_id, core_nede_id_id=news_id, core_content=content)



def model2json(data):
    array = []
    flag = True
    for ech in data:
        _json = model_to_dict(ech)
        _json.setdefault("pk", str(ech.pk))
        array.append(_json)

    # return json.dumps(array, ensure_ascii=False, default=__default).encode("utf-8")
    return array


#格式转换函数
def __default(obj):

    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')
    elif isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    elif isinstance(obj, UUID):
        return obj.__str__()
    else:
        raise TypeError('%r is not JSON serializable' % obj)


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
