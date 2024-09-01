from django.urls import path
from .views import load_data_view, generate_summary_report

urlpatterns = [
    path('load-data/', load_data_view, name='load_data'),
    path('summary-report/', generate_summary_report, name='summary_report'),
]
