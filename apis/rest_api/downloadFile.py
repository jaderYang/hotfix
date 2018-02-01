from django.http import StreamingHttpResponse
from django.http import HttpResponse
from rest_framework.views import APIView
from apis.tool import mongoOperate
import os
import json

class DownloadFileClass(APIView):

    def get(self, request):
        #分段读取文件内容
        def file_iterator(file_name, chunk_size=512):
            with open(file_name, 'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        MD5 = request.GET.get('MD5')
        #找出MD5相关的历史数据
        #创建db 及files collction对象
        mongoOperateTool = mongoOperate.MongoOperate('test')

        #同类型源文件下载
        coll = mongoOperateTool.get_collection('files')
        same_md5_files =  mongoOperateTool.get_many_docs(coll, {'MD5': MD5})
        orgin_files = list(same_md5_files)
        if len(orgin_files) > 0:
            desFile = orgin_files[0]
            file_path = desFile['filepath']
            the_file_name = desFile['name']
            response = StreamingHttpResponse(file_iterator(file_path))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
            return response
        #同类型补丁文件下载
        patchColl = mongoOperateTool.get_collection('patches')
        same_md5_patchs =  mongoOperateTool.get_many_docs(patchColl, {'MD5': MD5})
        patch_files = list(same_md5_patchs)
        if len(patch_files) > 0:
            desPatch = patch_files[0]
            file_path = desPatch['filepath']
            patch_file_name = desPatch['name']
            response = StreamingHttpResponse(file_iterator(file_path))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(patch_file_name)
            print(response)
            return response

        return HttpResponse(json.dumps({'result': 0, 'errorMsg':'文件下载错误'}))
