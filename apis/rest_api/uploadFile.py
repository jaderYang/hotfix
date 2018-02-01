from django.shortcuts import render_to_response
from django.http import HttpResponse
from rest_framework.views import APIView
from apis.tool import bsdiffTool
from apis.tool import mongoOperate
from django.conf import settings
import time
import os
import json

serverHost = 'http://'+ settings.SERVER_ADDR + "/index/rest_api/ymm"

class UploadFileClass(APIView):

    '''
    upload file method
    '''
    def post(self, request):

        f = request.FILES.get('file')
        version = request.POST.get('version')
        if not version:
            return HttpResponse('error！version 不能为空')

        #创建db 及files collction对象
        mongoOperateTool = mongoOperate.MongoOperate('test')
        coll = mongoOperateTool.get_collection('files')

        #同名文件列表
        same_name_files = mongoOperateTool.get_many_docs(coll, {'name':f.name})
        sorted_files = sorted(same_name_files, key=lambda same_name_file: same_name_file['version'])
        if len(sorted_files) > 0:
            latestFile = sorted_files[-1]
            if not version > latestFile['version']:
                return HttpResponse('error！请保证version递增')

        #文件存到本地
        baseDir = os.path.dirname(os.path.abspath(__name__))
        uploadpath = os.path.join(baseDir, 'static','upload', version)
        if not os.path.isdir(uploadpath):
            os.mkdir(uploadpath)
        filename = os.path.join(uploadpath, f.name)
        print(filename)
        fobj = open(filename, 'wb')
        for fchunk in f.chunks():
            fobj.write(fchunk)
        fobj.close()

        #获取文件md5值
        patchTool = bsdiffTool.BsdiffTool()
        md5Code = patchTool.getFileMd5(filename)

        #生成下载地址
        downloadUrl = serverHost + "/download/?MD5=" + md5Code
        #清除相同内容文件
        condition = {'MD5':md5Code}
        newRecord = { 'name':f.name, 'version':version, 'filepath':filename, 'MD5':md5Code, 'time':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), 'fileUrl':downloadUrl}

        mongoOperateTool.update_collection_withCondition(coll, newRecord, condition)

        result = f.name + ' upload success'
        return HttpResponse(result)
