from django.shortcuts import render_to_response
from django.http import HttpResponse
from rest_framework.views import APIView

class ClassBasedView(APIView):
    """
    docstring
    """
    def get(self, request):
        """

        :param request:
        :return:
        """
        html = 'I am ClassBasedview get func.'
        return HttpResponse(html)

    def post(self, request):
        """

        :param request:
        :return:
        """
        title = 'I am ClassBasedview post func.'
        print('request: %s' % request.POST)
        param1 = request.POST.get('mychoice')
        print (param1)
        html = title + " mychoice is: " + str(param1)
        return HttpResponse(html)
