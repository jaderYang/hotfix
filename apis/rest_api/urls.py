from django.conf.urls import url
from django.conf.urls import include
from rest_framework import routers

from apis.rest_api import views
from apis.rest_api import uploadFile
from apis.rest_api import downloadFile
from apis.rest_api import manageFiles
from apis.rest_api import checkUpdate

from rest_framework.authentication import BasicAuthentication,   SessionAuthentication, TokenAuthentication
#debug_router = routers.DefaultRouter()
#debug_router.register(r'debug', views.BasedClassView, base_name='debug')

urlpatterns = [
    url(r'^ymm/$', views.ClassBasedView.as_view(), name='ymm'),
    url(r'^ymm/upload/', uploadFile.UploadFileClass.as_view(), name='upload'),
    url(r'^ymm/download/', downloadFile.DownloadFileClass.as_view(), name='download'),
    url(r'^ymm/managefiles/', manageFiles.ManageFiles.as_view(), name='manageFiles'),
    url(r'^ymm/checkupdate/', checkUpdate.CheckUpdateClass.as_view(authentication_classes=[]), name='checkupdate')
]
