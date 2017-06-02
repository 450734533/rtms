# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers
import json
import requests
import os
import time
import logging
import sys
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import parsers, renderers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from serializers import UserSerializer, GroupSerializer, CaseSerializer, ResultSerializer, FlowSerializer, \
    SuiteSerializer, AuthSerializer, AuthScript1Serializer, PlanScriptSerilizer
from backend.models import Case, Result, Flow, Suite, Auth, AuthScript1, Plan
from backend.script import log
from backend.script.api_common import get_result
from backend.tasks import cook_plan

log.initLogging('/home/raoxin/demo/demo/log')


class UserViewSet(viewsets.ModelViewSet):
    """
    允许查看和编辑user 的 API endpoint
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    允许查看和编辑group的 API endpoint
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

    def retrieve(self, request, *args, **kwargs):
        print 12212121
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        print 122121211111212
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        name = self.request.GET.get('name')
        remark = self.request.GET.get('remark')
        if name:
            return Case.objects.filter(Q(name=name)).order_by('id')
        elif remark:
            return Case.objects.filter(Q(remark=remark)).order_by('id')
        else:
            return Case.objects.all().order_by('id')

    @detail_route(methods=['get'])
    def execute(self, request, pk=None):
        case = self.get_object()
        case_id = int(case.id)
        url = case.url.encode('utf-8')
        header = eval(case.header.encode('utf-8'))
        args = eval(case.boby.encode('utf-8'))
        expect1 = eval(case.expect.encode('utf-8'))
        if (len(url) != 0) | (len(header) != 0) | (len(args) != 0):
            try:
                resp = requests.post(url, json=args, headers=header)
                resp.close()
                status_code = resp.status_code
                if status_code != 200:
                    logging.error('%d_fail' % case_id)
                    logging.info('%d_code:' % case_id + str(resp.status_code))
                    logging.info(resp.content)
                    result = resp.content
                    debug = 'Error'
                    return Response({
                        'except': False,
                        'url': url,
                        'header': header,
                        'args': args,
                        'status_code': status_code,
                        'result': result,
                        'debug': debug
                    })
                else:
                    result = resp.json()
                    if isinstance(result, dict) & isinstance(expect1, dict):
                        bool_expect = get_result(expect1, result)
                        if bool_expect:
                            debug = 'Success'
                            return Response({
                                'except': False,
                                'url': url,
                                'header': header,
                                'args': args,
                                'status_code': status_code,
                                'result': result,
                                'debug': debug
                            })
                        else:
                            print '3333333333'
                            print result
                            debug = 'Fail'
                            return Response({
                                'except': False,
                                'url': url,
                                'header': header,
                                'args': args,
                                'status_code': status_code,
                                'result': result,
                                'debug': debug
                            })
                    else:
                        return Response({'except': True, 'error': '返回结果和期望值必须为dict'})
            except Exception as e:
                logging.error(Exception, '%d_Exception' % case_id, e)
                return Response({'except': True, 'error': str(e.message)})
        else:
            return Response(status=status.HTTP_200_OK)
            # result1 = resp.json()
            # result2 = json.dumps(result1, ensure_ascii=False)
            # print result2
            # Result.objects.filter(caseId=case_id).delete()
            # resultId = str(result['data']['adList'][0]['adId'])
            # resultdict = {'caseId': case_id, 'resultall': result2, 'resultId': resultId, 'ret': str(result1['ret'])}
            # Result.objects.create(**resultdict)
            # Case.objects.all().filter(id=case_id).update(retId=resultId)

    @list_route(methods=['get'])
    def tree(self, request):
        """
        Tree api for element UI.
        """
        data = serializers.serialize('json', Case.objects.all())
        data_list = json.loads(data)
        tree = []
        item = {'id': 1, 'label': '用例', 'children': []}
        for i in range(0, len(data_list)):
            case_id = data_list[i]['pk']
            case_name = data_list[i]['fields']['name'].encode('utf-8')
            _item = {'id': case_id, 'label': case_name}
            item['children'].append(_item)
        tree.append(item)
        return Response({'status': True, 'tree': tree})


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    def get_queryset(self):
        caseId = self.request.GET.get('caseId')
        if caseId:
            return Result.objects.filter(Q(caseId=caseId)).order_by('-id')
        else:
            return Result.objects.all().order_by('-id')


class FlowViewSet(viewsets.ModelViewSet):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer

    def get_queryset(self):
        name = self.request.GET.get('name')
        if name:
            return Flow.objects.filter(Q(name=name)).order_by('id')
        else:
            return Flow.objects.all().order_by('id')

    @detail_route(methods=['get'])
    def execute(self, request, pk=None):
        flow = self.get_object()
        flow_id = int(flow.id)
        flow_cards = flow.cards.encode('utf-8')
        print '1111111111111', flow_id, type(flow_id)
        print '2222222222222', flow_cards, type(flow_cards)
        return Response(status=status.HTTP_200_OK)


class SuiteViewSet(viewsets.ModelViewSet):
    queryset = Suite.objects.all()
    serializer_class = SuiteSerializer


class AuthViewSet(viewsets.ModelViewSet):
    queryset = Auth.objects.all()
    serializer_class = AuthSerializer


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanScriptSerilizer

    def create(self, request, *args, **kwargs):
        request.data['create_time'] = time.strftime("%Y-%m-%d-%H:%M", time.localtime(int(time.time())))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    @detail_route(methods=['get'])
    def cases(self, request, pk=None):
        plan = self.get_object()  # 计划表
        case_list = eval(plan.cases_id)
        cases = []  # 返回给前端chooseCaseData的数据为[{},{}]
        for i in range(0, len(case_list)):
            case = Case.objects.get(pk=case_list[i])
            cases.append(
                {
                    'id': case.id,
                    'name': case.name,
                    'remark': case.remark
                }
            )
        if plan.flag != 'A':
            print 1212121323
            cook_plan(plan.id)
        return Response({'cases': cases})


class AuthScript1ViewSet(viewsets.ModelViewSet):
    queryset = AuthScript1.objects.all()
    serializer_class = AuthScript1Serializer

    def create(self, request, *args, **kwargs):
        auth_file = self.request.FILES.get('auth_jar')
        # 先保存上传文件到一个路径，然后把路径保存在数据库中
        if auth_file:
            time1 = int(time.time())
            time2 = time.strftime("%Y%m%d%H%M", time.localtime(time1))
            auth_script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'authentication')
            filename = os.path.join(auth_script_path, time2 + '_' + auth_file.name).encode('utf-8')
            fobj = open(filename, 'wb')
            for chrunk in auth_file.chunks():
                fobj.write(chrunk)
                fobj.close()
            return Response({'status': True, 'file_path': filename})  # file_path返回给前端的auth_jar使用，保存在数据库中
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        file_path = instance.auth_jar
        os.system('rm -rf %s' % file_path)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    # serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'status': True, 'token': token.key, 'username': username})
        else:
            return Response({'status': False, 'message': 'Unable to log in with provided credentials'})
