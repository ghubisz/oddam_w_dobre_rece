from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
#    path('', views.entry_welcome, name='welcome'),
#    path('products/', views.entry_welcome, name='products'),
    path('', views.Landing_Page.as_view(),name='Home'),
#    path('admin/', admin.site.urls),
    path('landing_page/', views.Landing_Page.as_view(), name='landing_page'),
    path('form/', views.AddDonation, name='form'),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('index/', views.index, name='index')

]



