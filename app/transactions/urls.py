from django.urls import path

from . import apis

urlpatterns = [
    path('', apis.AllTransactions.as_view(), name='transactions')
]