from django.shortcuts import render_to_response
from django.http import HttpResponse
from rest_framework.views import APIView
from apis.tool import bsdiffTool
from apis.tool import mongoOperate
from django.conf import settings
import time
import os
import json

serverHost = 'http://'+settings.SERVER_ADDR + "/index/rest_api/ymm"

class CheckUpdateClass(APIView):
    def post(self, request):
        print(request.body)
        params = json.loads(request.body)
        print(params)

        MD5 = params.get('MD5')
        version = params.get('version')

        patch_url = None
        latest_file_url = None
        old_file_url = None
        #找出MD5相关的历史数据
        #创建db 及files collction对象
        mongoOperateTool = mongoOperate.MongoOperate('test')
        coll = mongoOperateTool.get_collection('files')

        #同类型文件的最新版本
        same_md5_file =  mongoOperateTool.get_one_doc(coll, {'MD5': MD5})
        print('md5+++'+MD5)
        print(same_md5_file)
        if not same_md5_file:
            return HttpResponse(json.dumps({'result': 0, 'errorMsg':'文件MD5无效'}))
        old_file_url = same_md5_file['filepath']
        old_version = same_md5_file['version']
        all_same_files = mongoOperateTool.get_many_docs(coll, {'name': same_md5_file['name']})
        all_same_files_list = list(all_same_files);
        if not len(all_same_files_list) > 0:
            return HttpResponse(json.dumps({'result': 0, 'errorMsg':'文件MD5无效'}))

        #筛选最新上传的file
        latestFile = None
        sorted_all_same_files = sorted(all_same_files_list, key=lambda all_same_file: all_same_file['time'])
        latestFile = sorted_all_same_files[-1]
        if not latestFile['version'] > old_version:
            return HttpResponse(json.dumps({'result': 0, 'errorMsg':'没有可更新版本'}))
        latest_file_url = latestFile['filepath']

        #补丁version生成规则 原version : 新version
        #fix: 好像不需要version
        patch_name = latestFile['name']
        patch_version = old_version + ':' + latestFile['version']
        #查看是否生成过该补丁
        patchColl = mongoOperateTool.get_collection('patches')
        single_patch = mongoOperateTool.get_one_doc(patchColl, {'name': patch_name, 'version': patch_version})

        #若已存在则直接使用
        if single_patch:
            patch_url = single_patch['filepath']
        else:
            #获取文件目录
            baseDir = os.path.dirname(os.path.abspath(__name__))
            patches_path = os.path.join(baseDir, 'static','patches',patch_version)
            if not os.path.isdir(patches_path):
                os.mkdir(patches_path)
            patch_url = os.path.join(patches_path, patch_name)

        patchTool = bsdiffTool.BsdiffTool()
        patchTool.getPatch(old_file_url, latest_file_url, patch_url)
        md5Code = patchTool.getFileMd5(patch_url)

        patch_downloadUrl = serverHost + "/download/?MD5=" + md5Code
        latest_downloadUrl = serverHost + "/download/?MD5=" + latestFile['MD5']

        condition = {'MD5':md5Code}
        newRecord = {'name':patch_name, 'version':patch_version, 'filepath':patch_url, 'MD5':md5Code, 'time':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), 'fileUrl': patch_downloadUrl}

        mongoOperateTool.update_collection_withCondition(patchColl, newRecord, condition)
        # uploadTip 0.建议升级 1.强制升级 2.静默升级
        return HttpResponse(json.dumps({'result': 1, 'fileUrl': latest_downloadUrl,'fileMd5':latestFile['MD5'], 'patchUrl': patch_downloadUrl, 'patchMd5':md5Code, 'version':latestFile['version'], 'uploadTip':'1'}))
