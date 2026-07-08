from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from apps.dashboard.api import DashboardStatsAPIView
from apps.jobs.api import JobDetailAPIView, JobListAPIView
from apps.applications.api import ApplicationDetailAPIView, ApplicationListAPIView
from apps.resumes.api import ResumeListAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='dashboard:index', permanent=False)),
    path('account/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('api/dashboard/stats/', DashboardStatsAPIView.as_view(), name='dashboard-stats'),
    path('api/jobs/', JobListAPIView.as_view(), name='jobs-list-api'),
    path('api/jobs/<int:pk>/', JobDetailAPIView.as_view(), name='job-detail-api'),
    path('api/applications/', ApplicationListAPIView.as_view(), name='applications-list-api'),
    path('api/applications/<int:pk>/', ApplicationDetailAPIView.as_view(), name='application-detail-api'),
    path('api/resumes/', ResumeListAPIView.as_view(), name='resumes-list-api'),
    path('jobs/', include('apps.jobs.urls')),
    path('candidates/', include('apps.applications.urls')),
    path('resumes/', include('apps.resumes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)