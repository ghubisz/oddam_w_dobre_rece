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
    path('AddDonation/', views.AddDonation, name='add_donation', id='giveaway-form'),
    path('Login/', views.Login, name='login', id='login-page'),
    path('Register/', views.Register, name='register', id='register-page')

]



