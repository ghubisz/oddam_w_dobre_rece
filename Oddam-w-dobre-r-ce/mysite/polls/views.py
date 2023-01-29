from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Category
from .models import Institution
from .models import Donation
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model, login
import ipdb
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import ExpressionWrapper, F, DateTimeField
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from .forms import (
    AddDonationFormStepOne,
    AddDonationFormStepTwo,
    AddDonationFormStepThree,
    AddDonationStepFour,
    AddDonationFormStepFive,
    LoginForm,
    UserEditForm,
    UserPasswordChangeForm,
    UserCreationForm,
    SignUpForm)

from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    FormView,
    TemplateView
)
from .tokens import email_verification_token
from formtools.wizard.views import SessionWizardView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import ipdb
from django.conf import settings



#def index(request):
#    queryset = Category.objects.all()
#    context = {
#       'queryset': queryset
#        #        'user_id': request.user.id
#    }
#    return TemplateResponse(request, 'index.html', context)
#    # return HttpResponse("Hello, world. You're at the polls index.")
#    #return TemplateResponse(request, 'login.html', context)
#    #return HttpResponse(request, index.html, context)

class Index(View):
        def get(self, request, *args, **kwargs):
            donations = Donation.objects.all()
            foundations = Institution.objects.filter(institution_type='FUND')
            charity = Institution.objects.filter(institution_type='CHAR')
            quantity = sum([donation.quantity for donation in donations])
            institutions = len(set([donation.institution_id for donation in
                                    donations]))
#TODO zmienic pag na 5
            found_paginator = Paginator(foundations, 3)
            page = request.GET.get('page1')
            try:
                paged_foundations = found_paginator.page(page)
            except PageNotAnInteger:
                paged_foundations = found_paginator.page(1)
            except EmptyPage:
                paged_foundations = found_paginator.page(found_paginator.num_pages)

            ngos = Institution.objects.filter(institution_type='NGOV')
            ngos_paginator = Paginator(ngos, 3)

 #           found_paginator = Paginator(foundations, 3)
            page = request.GET.get('page2')
            try:
                paged_ngos = ngos_paginator.page(page)
            except PageNotAnInteger:
                paged_ngos = ngos_paginator.page(1)
            except EmptyPage:
                paged_ngos = ngos_paginator.page(ngos_paginator.num_pages)



            charity = Institution.objects.filter(institution_type='CHAR')
            charity_paginator = Paginator(charity, 2)

 #           found_paginator = Paginator(foundations, 3)
            page = request.GET.get('page3')
            try:
                paged_charity = charity_paginator.page(page)
            except PageNotAnInteger:
                paged_charity = charity_paginator.page(1)
            except EmptyPage:
                paged_charity = charity_paginator.page(charity_paginator.num_pages)

#            page_number = request.GET.get('foundations')
 #           foundations = found_paginator.get_page(page_number)
  #          page_number = request.GET.get('page2')
   #         ngos = ngos_paginator.get_page(page_number)
    #        page_number = request.GET.get('page3')
     #       charities = charity_paginator.get_page(page_number)


            context = {
                'quantity': quantity,
                'institutions': institutions,
                'foundations': paged_foundations,
                'ngos': paged_ngos,
                'charity': paged_charity
                #            'queryset': queryset
                #            'user_id': request.user.id
            }
            return render(request, 'index.html', context)
        # return HttpResponse("Hello, world. You're at the polls index.")

class Landing_Page(View):
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

class Login(LoginView):

    form_class = LoginForm
    template_name = "login.html"


class Register(SuccessMessageMixin, CreateView):
    model = get_user_model()
    form_class = SignUpForm
    template_name = "register.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):

        user = form.save(commit=False)
        to_email = form.cleaned_data.get('email')
        user.username = to_email
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Proszę o aktywację konta na charity - donation.'
        message = render_to_string('to_activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': email_verification_token.make_token(user),
        })

        email = EmailMessage(
                mail_subject,message, to=[to_email]

        )
        email.send()
        return super(RegisterView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return "Konto pomyślnie zarezerwowane! Wymagana aktywacja przez adres email."



    # return HttpResponse("Hello, world. You're at the polls index.")
    #return TemplateResponse(request, 'login.html', context)
    #return TemplateResponse(request, 'register.html', context)

class AddDonationView(SessionWizardView):
    form_list = (
        AddDonationFormStepOne,
        AddDonationFormStepTwo,
        AddDonationFormStepThree,
        AddDonationStepFour,
        AddDonationFormStepFive

    )
    def get_context_data(self, form, **kwargs):
        context = super(AddDonationView, self).get_context_data(form, **kwargs)
        context['categories'] = Category.objects.all()
        context['institutions'] = Institution.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        try:
            return self.render(self.get_form())
        except KeyError:
            return super().get(request, *args, **kwargs)

    def get_form_initial(self, step):
        if step == '2':
            step0data = self.get_cleaned_data_for_step('0')
            if step0data:
                categories = step0data.get('categories', '')
                return self.initial_dict.get(step, {'categories': categories})
        return self.initial_dict.get(step, {})

    def done(self, form_list, **kwargs):
        form_data = [form.cleaned_data for form in form_list]
        categories = form_data[0]['categories']
        donation = Donation.objects.create(
            quantity = form_data[1]['quantity'],
            institution = form_data[2]['institution'],
            address = form_data.cleaned_data['address'],
            city = form_data.cleaned_data['city'],
            zip_code = form_data.cleaned_data['zip_code'],
            phone_number = form_data.cleaned_data['phone_number'],
            pick_up_date = form_data.cleaned_data['pick_up_date'],
            pick_up_time = form_data.cleaned_data['pick_up_time'],
            pick_up_comment = form_data.cleaned_data['pick_up_comment'],
            user=self.request.user

        )
        donation.categories.set(categories)
        return render(self.request,'form-confirmation.html', {'form_data': [
            form.cleaned_data for form in form_list]})

#class Activate(View):
#    template_name = 'login.html'

#    def get(self, request, uidb64, token):
#        try:
#            uid = force_text(urlsafe_base64_decode(uidb64))
#            user = User.objects.get(pk=uid)

#        except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
#            user = None
#        if user is not None and email_verification_token.check_token(user, token):
#            user.is_active = True
#            user.save()
#            messages.add_message(request, messages.INFO, 'Konto aktywne. Możesz się teraz zalogować.')
#            return render(request, self.template_name)
#        else:
#            messages.add_message(request, messages.WARNING, 'Link aktywacyjny wygasł.')
#            return render(request, self.template_name)

class ProfileView(UserPassesTestMixin, LoginRequiredMixin, DetailView):

#    model = CustomUser
#    template_name = 'profile.html'
#    pk_url_kwarg = 'pk'

    def test_func(self):
        return self.request.user == self.get_object()

class UserEditView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):

    template_name = 'edit_profile.html'
    form_class = UserEditForm
    success_url = reverse_lazy('landing-page')

    def get_object(self):
        return self.request.user

    def get_success_message(self, cleaned_data):
        return "Twoje dane zostały zmienione!"

class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):

    template_name = 'change_password.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('landing-page')

    def get_success_message(self, cleaned_data):
        return "Twoje hasło zostało zmienione!"

class DonationListView(LoginRequiredMixin, View):

    template_name = 'donations.html'

    def get(self, request, *args, **kwargs):
        """ Creates new field 'my_dt' on model Donation to filter by combined two other model's fields: Date and Time Field.
         Pass the results to context."""
        user_donations = Donation.objects.annotate(
            my_dt = ExpressionWrapper(F('pick_up_date')+F('pick_up_time'),
                                      output_field=DateTimeField())).filter(
            user= request.user)
        picked_up = user_donations.filter(my_dt__lt=timezone.now())
        ordered = user_donations.filter(my_dt__gt=timezone.now())
        context = {

            'picked_up': picked_up,
            'ordered': ordered,
        }
        return render(request, self.template_name, context)

class DonaionDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):

    model = Donation
    template_name = 'donation_detail.html'
    pk_url_kwarg = 'pk'

    def test_func(self):
        """Forbidden access to the view if object Donation not belong to
        request.user
        """
        return self.request.user == self.get_object().user

class SignUp(View):
    form_class = SignUpForm
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
       # ipdb.set_trace()

        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('to_activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token': email_verification_token.make_token(user),
            })


            #Todo: Add try catch
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                subject, message, to=[to_email]
            )
            email.content_subtype = "html"
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            return HttpResponse('Form invalid')


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        ipdb.set_trace()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and email_verification_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('home')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')