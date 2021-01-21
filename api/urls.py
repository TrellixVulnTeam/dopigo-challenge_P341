""" URLs module of DOPIGO Challenge / API App """
from rest_framework import routers
from django.conf.urls import include, re_path, url
from . import views

router = routers.SimpleRouter()

router.register('create-account', views.AccountViewSet, basename='create-account')
router.register('retrieve-action', views.ActionViewSet, basename='retrieve-action')
router.register('check-balance', views.BalanceViewSet, basename='check-balance')
router.register('create-transfer', views.MoneyTransferViewSet, basename='create-transfer')

urlpatterns = [
    re_path('^', include(router.urls)),
]