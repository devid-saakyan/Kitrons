from django.urls import path
from .views import *

urlpatterns = [
    path('GetNewsFeed', GetNewsFeedView.as_view(), name='GetCompanies'),
    path('GetNewsById/<int:pk>/', GetNewsFeedByIdView.as_view(), name='GetCompaniesById'),
    path('GetNewsByCompanyId/<int:companyId>/', GetNewsFeedByCompanyId.as_view(), name='GetCompaniesById'),
]