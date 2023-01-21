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
    path('form/', views.AddDonation, name='form'),
    path('login/', views.Login, name='login'),
    path('register/', views.Register, name='register'),
    path('index/', views.index, name='index')

]



