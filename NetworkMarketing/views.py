from django.shortcuts import HttpResponse


def Homepage(request):
    return HttpResponse('This is Home pAge')
