from django.shortcuts import render
from django.shortcuts import HttpResponse

def renderhelper(request, folder, html_page, context={}):
    return render(request, 'superadmin/' + folder + '/' + html_page + '.html', context)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'