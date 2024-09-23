from django.urls import path
from .views import GetAdsView, GetAdsByIdView, GetAdsByCompanyIdView, GetAdsQuestionView, ApplyAnswerView, UserAdsHistoryView

urlpatterns = [
    path('GetAds/', GetAdsView.as_view(), name='get_ads'),
    path('GetAdsById/<int:pk>/', GetAdsByIdView.as_view(), name='get_ads_by_id'),
    path('GetAdsByCompanyId/<int:companyId>/', GetAdsByCompanyIdView.as_view(), name='get_ads_by_company_id'),
    path('GetAdsQuestion/<int:AdId>/', GetAdsQuestionView.as_view(), name='get_ads_question'),
    path('ApplyAnswer/', ApplyAnswerView.as_view(), name='apply_answer'),
    path('UserAdsHistory/', UserAdsHistoryView.as_view(), name='user_ads_history'),
]
