from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Category
from .models import Institution
from .models import Donation
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
import ipdb
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.db.models import ExpressionWrapper, F, DateTimeField
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    FormView,
    TemplateView
)


def index(request):
    queryset = Category.objects.all()
    context = {
        'queryset': queryset
        #        'user_id': request.user.id
    }
    return TemplateResponse(request, 'index.html', context)
    # return HttpResponse("Hello, world. You're at the polls index.")
    #return TemplateResponse(request, 'login.html', context)
    #return HttpResponse(request, index.html, context)

def Landing_Page(request):
    def get(self, request, *args, **kwargs):
        donations = Donation.objects.all()
        foundations = Institution.objects.filter(institution_type='FUND')
        charity = Institution.objects.filter(institution_type='CHAR')
        quantity = sum([donation.quantity for donation in donations])
        institutions = len(set([donation.institution_id for donation in
                                donations]))

        found_paginator = Paginator(foundations, 5)
        ngos = Institution.objects.filter(institution_type='NGOV')
        ngos_paginator = Paginator(ngos, 5)
        charity = Institution.objects.filter(institution_type='CHAR')
        charity_paginator = Paginator(charity, 5)

        page_number = request.GET.get('foundations')
        foundations = found_paginator.get_page(page_number)
        page_number = request.GET.get('page2')
        ngos = ngos_paginator.get_page(page_number)
        page_number = request.GET.get('page3')
        charities = charity_paginator.get_page(page_number)

        context = {
            'quantity': quantity,
            'institutions': institutions,
            'foundations': foundations,
            'ngos': ngos,
            'charitiy': charity
#            'queryset': queryset
#            'user_id': request.user.id
    }
        return render(request, 'index.html', context)
    #return HttpResponse("Hello, world. You're at the polls index.")


def AddDonation(request):
    queryset = Category.objects.all()

    context = {
        'queryset': queryset
        #        'user_id': request.user.id
    }
    return TemplateResponse(request, 'form.html', context)
    # return HttpResponse("Hello, world. You're at the polls index.")
    #return TemplateResponse(request, 'login.html', context)
    #return TemplateResponse(request, 'form-confirmation.html', context)

def Login(request):
    queryset = Category.objects.all()
    context = {
        'queryset': queryset
        #        'user_id': request.user.id
    }
    return TemplateResponse(request, 'login.html', context)
    # return HttpResponse("Hello, world. You're at the polls index.")
    #return TemplateResponse(request, 'login.html', context)

def Register(request):
    queryset = Category.objects.all()
    context = {
        'queryset': queryset
        #        'user_id': request.user.id
    }
    return TemplateResponse(request, 'register.html', context)
    # return HttpResponse("Hello, world. You're at the polls index.")
    #return TemplateResponse(request, 'login.html', context)
    #return TemplateResponse(request, 'register.html', context)
