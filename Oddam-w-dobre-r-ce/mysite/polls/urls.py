from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
#    path('', views.entry_welcome, name='welcome'),
#    path('products/', views.entry_welcome, name='products'),
    path('', views.Index.as_view(), name='home'),
#    path('admin/', admin.site.urls),
    path('landing_page/', views.Landing_Page.as_view(), name='landing_page'),
    path('form/', views.AddDonation, name='form'),
    path('login/', views.Login.as_view(), name='login'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('index/', views.Index.as_view(), name='index'),
    path('activate/<uid64>/<token>/', views.ActivateAccount.as_view(), name='activate')

]



