from datetime import date, datetime
import json
from uuid import UUID

import simplejson
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
import uuid
from app_server.ModelForm.LoginRegistFrom import LoginFrom, RegistFrom
from .models import *


def index(request):
    res = {}
    req = json.loads(request.body)
    operation = req['operation']
    page = req['page']

    res_list = NewsDetail.objects.order_by('nede_create_date').all()
    tablelen = res_list.count()

    if tablelen == 0:
        print('服务器无数据')
        res['msg'] = '404'
        res['success'] = 'false'
        res['data'] = []
        res_json = json.dumps(res, ensure_ascii=False, default=__default).encode("utf-8")
        return HttpResponse(res_json, content_type="application/json; charset=utf-8")
    else:
        start = (page-1) * 10
        end = page * 10 - 1
        # 已经完全取完
        if start >= tablelen:
            print('数据已取完')
            res['msg'] = '404'
            res['success'] = 'false'
            res['data'] = []
            res_json = json.dumps(res, ensure_ascii=False, default=__default).encode("utf-8")
            return HttpResponse(res_json, content_type="application/json; charset=utf-8")

        if end > tablelen:
            end = tablelen - 1
        _json = model2json(res_list[start:end])
        res['msg'] = '200'
        res['success'] = 'true'
        res['data'] = _json
        print('正常取数据')
        res_json = json.dumps(res, ensure_ascii=False, default=__default).encode("utf-8")
        return HttpResponse(res_json, content_type="application/json; charset=utf-8")


def result(request):
    res = {}

    req = json.loads(request.body)
    # 这里需要更改
    # classify = req['classify']
    classify = '国产动漫'
    res_list = NewsDetail.objects.filter(nede_classify=classify)
    _json = model2json(res_list)
    res['msg'] = '200'
    res['success'] = 'true'
    res['data'] = _json

    res_json = simplejson.dumps(res).encode('utf-8').decode('unicode-escape')
    print('已获取classify\n' + classify)
    return HttpResponse(res_json, content_type="application/json; charset=utf-8")


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
    req = simplejson.loads(request.body)
    core_nede_id = req['news_id']
    print(core_nede_id)
    try:
        comment_list = CommentReplay.objects.filter(core_nede_id_id=core_nede_id)
        # _json = model2json(comment_list)
        # 若评论为空
        if comment_list.count() == 0:
            res['msg'] = '404'
            res['success'] = 'false'
            return HttpResponse(json.dumps(res).encode('utf-8').decode('unicode-escape'), content_type="application/json; charset=utf-8")

        # 最笨的方法，在循环里面再写查询，先把自己鄙视一番
        for m in comment_list:
            comment_data = {}
            n = UserInfo.objects.get(usin_id_id=m.core_acco_id_id)
            comment_data['content'] = m.core_content
            comment_data['name'] = n.usin_name
            comment_data['time'] = str(m.core_date)
            # comment_data['id'] = str(m.id)
            comment.append(comment_data)

        res['msg'] = '200'
        res['success'] = 'true'
        res['data'] = comment
    except:
        res['msg'] = '302'
        res['success'] = 'false'

    finally:
        res_json = json.dumps(res).encode('utf-8').decode('unicode-escape')
        return HttpResponse(res_json, content_type="application/json; charset=utf-8")


def deliver_comment(request):
    res = {}
    req = simplejson.loads(request.body)
    content = req['comment_content']
    user_id = int(req['user_id'])
    news_id = uuid_without(req['news_id'])
    try:
        CommentReplay.objects.create(core_nede_id_id=news_id, core_acco_id_id=user_id, core_content='hello')
        res['msg'] = '200'
        res['success'] = 'true'
    except:
        res['msg'] = '302'
        res['success'] = 'false'

    res_json = json.dumps(res).encode('utf-8').decode('unicode-escape')
    return HttpResponse(res_json, content_type="application/json; charset=utf-8")


def model2json(data):
    array = []
    flag = True
    for ech in data:
        _json = model_to_dict(ech)
        _json.setdefault("pk", str(ech.pk))
        array.append(_json)

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


# uuid转换去掉'-'
def uuid_without(news_id):
    s_uuid = news_id
    l_uuid = s_uuid.split('-')
    s_uuid = ''.join(l_uuid)
    return s_uuid
