from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Category
from .models import Institution
from .models import Donation
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user
import ipdb


def index(request):
    return HttpResponse(request, index.html, context)

def Landing_Page(request):
    queryset = Category.objects.all()
    context = {
        'queryset': queryset
#        'user_id': request.user.id
    }
    return TemplateResponse(request, 'index.html',context)
    #return HttpResponse("Hello, world. You're at the polls index.")


def AddDonation(request):
    return TemplateResponse(request, 'form-confirmation.html', context)

def Login(request):
    return TemplateResponse(request, 'login.html', context)

def Register(request):
    return TemplateResponse(request, 'register.html', context)
