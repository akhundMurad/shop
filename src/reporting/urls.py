from django.urls import path, include

from reporting.views import report

app_name = 'reporting'

report_patterns = [
    path(
        '',
        report.ReportListAPIView.as_view(),
        name='report-list'
    )
]

urlpatterns = [
    path('report/', include(report_patterns))
]
