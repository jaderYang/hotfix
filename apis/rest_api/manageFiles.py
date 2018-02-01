from django.shortcuts import render_to_response
from django.http import HttpResponse
from rest_framework.views import APIView
import os
from apis.tool import mongoOperate
import json

class ManageFiles(APIView):

    def get(self, request):
        '''
            获取文件列表：type: file 为源文件， patch为补丁包
        '''
        result = []
        resultList = []
        resultObj = {}
        mongoOperateTool = mongoOperate.MongoOperate('test')
        # files list query
        fileColl = mongoOperateTool.get_collection('files')
        result = mongoOperateTool.get_many_docs(fileColl, {})
        for item in result:
            item.pop('_id')
            resultList.append(item)
        resultObj['files'] = resultList;

        #patchs list query
        patchColl = mongoOperateTool.get_collection('patches')
        result = mongoOperateTool.get_many_docs(patchColl, {})
        resultList = [];
        for item in result:
            item.pop('_id')
            resultList.append(item)
        resultObj['patchs'] = resultList;
        #json stringify dict
        return HttpResponse(json.dumps(resultObj))
