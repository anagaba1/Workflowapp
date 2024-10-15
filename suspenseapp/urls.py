from django.urls import path
from .import views
#from suspenseapp.views import suspensesearch


urlpatterns = [

    path('msp_search/', views.suspensesearch, name='msp_search'),
    path('esp_search/', views.empl_suspensesearch, name='esp_search'),
    path('nsf_search/', views.nsf_suspensesearch, name='nsf_search'),
    
]
