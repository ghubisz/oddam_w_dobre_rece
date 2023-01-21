from django.urls import path
from django.urls import include
from .views import *
from . import views

urlpatterns = [
#    path('', views.entry_welcome, name='welcome'),
#    path('products/', views.entry_welcome, name='products'),
    path('', views.Landing_Page,name='Home'),
#    path('admin/', admin.site.urls),
    path('landing_page/', views.Landing_Page, name='landing_page'),
    path('AddDonation/#giveaway-form', views.AddDonation, name='add_donation'),
    path('Login/#login-page', views.Login, name='login'),
    path('Register/#register-page', views.Register, name='register')

]



