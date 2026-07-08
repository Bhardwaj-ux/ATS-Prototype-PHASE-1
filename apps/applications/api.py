from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from .models import Application


class ApplicationListAPIView(LoginRequiredMixin, View):
    def get(self, request):
        applications = list(
            Application.objects.select_related('job')
            .order_by('-created_at')
            .values(
                'id',
                'full_name',
                'email',
                'phone',
                'current_location',
                'total_experience_years',
                'source',
                'status',
                'skills',
                'created_at',
                'job__title',
            )
        )
        return JsonResponse({'applications': applications})


class ApplicationDetailAPIView(LoginRequiredMixin, View):
    def get(self, request, pk):
        application = Application.objects.select_related('job').filter(pk=pk).first()
        if not application:
            return JsonResponse({'error': 'Application not found.'}, status=404)

        payload = {
            'id': application.id,
            'full_name': application.full_name,
            'email': application.email,
            'phone': application.phone,
            'current_location': application.current_location,
            'total_experience_years': str(application.total_experience_years),
            'source': application.source,
            'status': application.status,
            'summary': application.summary,
            'skills': application.skill_list(),
            'job_title': application.job.title if application.job else None,
            'created_at': application.created_at.isoformat(),
        }
        return JsonResponse({'application': payload})
