from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import
from .models import

def Landing_Page(request):
    return TemplateRespone(request,base.html, context)

def AddDonation(request):
    return TemplateResponse(request,,context)

def Login(request):
    return TemplateResponse(request, ,context)

def Register(request):
    return TemplateResponse(request, , context)
