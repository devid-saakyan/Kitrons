from django.urls import path
from .views import *

urlpatterns = [
    path('GetCompanies', GetCompanyList.as_view(), name='GetCompanies'),
    path('GetCompanyById/<int:pk>/', GetCompanyById.as_view(), name='GetCompaniesById'),
]