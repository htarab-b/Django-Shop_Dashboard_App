from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('orderlist/', OrderlistView.as_view(), name='orderlist'),
    path('download/', DownloadView.as_view(), name='download'),
    path('order/', Order.as_view(), name='order'),
    path('changedeliverystatus/', ChangeDeliveryStatus.as_view(), name='changedeliverystatus'),
    path('shopapi/', ShopAPIView.as_view(), name='shop-api'),
    path('orderapi/', OrderAPIView.as_view(), name='order-api'),
]