from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from .models import Job


class JobListAPIView(LoginRequiredMixin, View):
    def get(self, request):
        jobs = list(
            Job.objects.filter(is_active=True)
            .order_by('-created_at')
            .values(
                'id',
                'title',
                'department',
                'location',
                'employment_type',
                'status',
                'experience_min_years',
                'experience_max_years',
                'created_at',
            )
        )
        return JsonResponse({'jobs': jobs})


class JobDetailAPIView(LoginRequiredMixin, View):
    def get(self, request, pk):
        job = Job.objects.filter(pk=pk, is_active=True).first()
        if not job:
            return JsonResponse({'error': 'Job not found.'}, status=404)

        payload = {
            'id': job.id,
            'title': job.title,
            'department': job.department,
            'location': job.location,
            'employment_type': job.employment_type,
            'status': job.status,
            'experience_min_years': job.experience_min_years,
            'experience_max_years': job.experience_max_years,
            'description': job.description,
            'requirements': job.requirements,
            'created_at': job.created_at.isoformat(),
        }
        return JsonResponse({'job': payload})
