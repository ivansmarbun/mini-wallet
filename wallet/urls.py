from django.urls import path

from . import views


app_name = "insurance"

urlpatterns = [
    path('init', views.create_wallet, name='create_wallet'),
    path('wallet', views.enable_disable_wallet, name='enable_disable_wallet'),
    path('wallet/deposit', views.deposit_wallet, name='deposit_wallet'),
    path('wallet/withdraw', views.withdraw_wallet, name='withdraw_wallet')
]
